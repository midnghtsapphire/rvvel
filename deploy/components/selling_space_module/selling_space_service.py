"""Selling Space Service — Self-service ad platform across all domains."""
import uuid
from typing import Optional, Dict, List
from datetime import datetime, timezone, timedelta

SELLING_SPACE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS ad_placements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    advertiser_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url TEXT,
    click_url TEXT NOT NULL,
    ad_tier VARCHAR(20) NOT NULL,
    placement_type VARCHAR(20) NOT NULL DEFAULT 'sidebar',
    target_domains TEXT[] DEFAULT ARRAY[]::TEXT[],
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    stripe_payment_id VARCHAR(255),
    amount_paid_cents INTEGER NOT NULL DEFAULT 0,
    impressions INTEGER NOT NULL DEFAULT 0,
    clicks INTEGER NOT NULL DEFAULT 0,
    starts_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ad_impressions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ad_id UUID NOT NULL REFERENCES ad_placements(id),
    page_url TEXT,
    ip_hash VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ad_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ad_id UUID NOT NULL REFERENCES ad_placements(id),
    ip_hash VARCHAR(64),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ad_placements_status ON ad_placements(status, starts_at, expires_at);
CREATE INDEX IF NOT EXISTS idx_ad_placements_advertiser ON ad_placements(advertiser_id);
"""

AD_TIERS = {
    "basic": {"price_cents": 2000, "max_impressions": 5000, "placement": ["sidebar"]},
    "standard": {"price_cents": 5000, "max_impressions": 15000, "placement": ["sidebar", "footer"]},
    "premium": {"price_cents": 10000, "max_impressions": 50000, "placement": ["sidebar", "footer", "inline"]},
    "featured": {"price_cents": 20000, "max_impressions": 100000, "placement": ["banner", "sidebar", "inline"]},
    "spotlight": {"price_cents": 50000, "max_impressions": 300000, "placement": ["all"]},
    "exclusive": {"price_cents": 100000, "max_impressions": 750000, "placement": ["all"]},
    "domination": {"price_cents": 200000, "max_impressions": None, "placement": ["all"]},
}


class SellingSpaceService:
    def __init__(self, db_pool):
        self.db = db_pool

    async def create_ad(self, advertiser_id: str, title: str, description: str,
                        image_url: str, click_url: str, ad_tier: str,
                        placement_type: str, target_domains: List[str],
                        duration_days: int = 30) -> Dict:
        if ad_tier not in AD_TIERS:
            return {"error": f"Invalid tier: {ad_tier}"}

        ad_id = str(uuid.uuid4())
        starts_at = datetime.now(timezone.utc)
        expires_at = starts_at + timedelta(days=duration_days)

        async with self.db.acquire() as conn:
            await conn.execute(
                """INSERT INTO ad_placements
                   (id, advertiser_id, title, description, image_url, click_url,
                    ad_tier, placement_type, target_domains, status, starts_at, expires_at,
                    amount_paid_cents)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,'pending',$10,$11,$12)""",
                ad_id, advertiser_id, title, description, image_url, click_url,
                ad_tier, placement_type, target_domains, starts_at, expires_at,
                AD_TIERS[ad_tier]["price_cents"]
            )

        return {"ad_id": ad_id, "status": "pending", "tier": ad_tier,
                "price_cents": AD_TIERS[ad_tier]["price_cents"]}

    async def activate_ad(self, ad_id: str, stripe_payment_id: str) -> Dict:
        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE ad_placements
                   SET status = 'active', stripe_payment_id = $2, updated_at = NOW()
                   WHERE id = $1""",
                ad_id, stripe_payment_id
            )
        return {"ad_id": ad_id, "status": "active"}

    async def get_active_ads(self, domain: str = "", placement: str = "", limit: int = 5) -> List[Dict]:
        async with self.db.acquire() as conn:
            query = """SELECT id, title, description, image_url, click_url, ad_tier, placement_type
                       FROM ad_placements
                       WHERE status = 'active' AND starts_at <= NOW() AND expires_at > NOW()"""
            params = []
            if domain:
                query += f" AND ($1 = ANY(target_domains) OR target_domains = '{{}}')"
                params.append(domain)
            query += f" ORDER BY RANDOM() LIMIT {limit}"
            rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]

    async def record_impression(self, ad_id: str, page_url: str = "", ip_hash: str = ""):
        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO ad_impressions (ad_id, page_url, ip_hash) VALUES ($1, $2, $3)",
                ad_id, page_url, ip_hash
            )
            await conn.execute(
                "UPDATE ad_placements SET impressions = impressions + 1 WHERE id = $1", ad_id
            )

    async def record_click(self, ad_id: str, ip_hash: str = "", user_agent: str = ""):
        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO ad_clicks (ad_id, ip_hash, user_agent) VALUES ($1, $2, $3)",
                ad_id, ip_hash, user_agent
            )
            await conn.execute(
                "UPDATE ad_placements SET clicks = clicks + 1 WHERE id = $1", ad_id
            )

    async def get_advertiser_stats(self, advertiser_id: str) -> Dict:
        async with self.db.acquire() as conn:
            ads = await conn.fetch(
                "SELECT * FROM ad_placements WHERE advertiser_id = $1 ORDER BY created_at DESC",
                advertiser_id
            )
        return {"ads": [dict(a) for a in ads], "total_ads": len(ads)}
