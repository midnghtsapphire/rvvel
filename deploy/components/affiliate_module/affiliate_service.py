"""Affiliate Service — Auto-generate affiliate links, track clicks and conversions."""
import os
import re
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse, parse_qs


@dataclass
class AffiliateConfig:
    amazon_tag: str = ""
    amazon_access_key: str = ""
    amazon_secret_key: str = ""
    base_url: str = "https://glowstarlabs.com"

    def __post_init__(self):
        if not self.amazon_tag:
            self.amazon_tag = os.environ.get("AMAZON_ASSOCIATES_TAG", "glowstarlabs-20")
        if not self.amazon_access_key:
            self.amazon_access_key = os.environ.get("AMAZON_ACCESS_KEY", "")


AFFILIATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS affiliate_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(500) NOT NULL,
    original_url TEXT NOT NULL,
    affiliate_url TEXT NOT NULL,
    short_code VARCHAR(20) UNIQUE NOT NULL,
    amazon_asin VARCHAR(20),
    category VARCHAR(100),
    source_module VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    link_id UUID NOT NULL REFERENCES affiliate_links(id),
    user_id UUID,
    ip_hash VARCHAR(64),
    user_agent TEXT,
    referrer TEXT,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_conversions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    link_id UUID NOT NULL REFERENCES affiliate_links(id),
    user_id UUID,
    order_id VARCHAR(255),
    amount_cents INTEGER,
    commission_cents INTEGER,
    converted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_affiliate_links_code ON affiliate_links(short_code);
CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_link ON affiliate_clicks(link_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_conversions_link ON affiliate_conversions(link_id);
"""


class AffiliateService:
    """Auto-generate and track affiliate links for product mentions."""

    def __init__(self, db_pool, config: Optional[AffiliateConfig] = None):
        self.db = db_pool
        self.config = config or AffiliateConfig()

    def generate_amazon_link(self, url: str) -> str:
        """Add Amazon Associates tag to any Amazon URL."""
        parsed = urlparse(url)
        if "amazon.com" not in parsed.netloc and "amzn.to" not in parsed.netloc:
            return url
        params = parse_qs(parsed.query)
        params["tag"] = [self.config.amazon_tag]
        new_query = urlencode(params, doseq=True)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

    def generate_amazon_search_link(self, product_name: str) -> str:
        """Generate Amazon search affiliate link for a product name."""
        params = {"k": product_name, "tag": self.config.amazon_tag}
        return f"https://www.amazon.com/s?{urlencode(params)}"

    def generate_amazon_asin_link(self, asin: str) -> str:
        """Generate direct Amazon product link from ASIN."""
        return f"https://www.amazon.com/dp/{asin}?tag={self.config.amazon_tag}"

    async def create_tracked_link(
        self, product_name: str, original_url: str,
        category: str = "", source_module: str = "", asin: str = ""
    ) -> Dict:
        """Create a tracked affiliate link with short code."""
        affiliate_url = self.generate_amazon_link(original_url)
        short_code = uuid.uuid4().hex[:8]

        async with self.db.acquire() as conn:
            await conn.execute(
                """INSERT INTO affiliate_links
                   (product_name, original_url, affiliate_url, short_code, amazon_asin, category, source_module)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                product_name, original_url, affiliate_url, short_code, asin, category, source_module
            )

        return {
            "short_code": short_code,
            "tracked_url": f"{self.config.base_url}/go/{short_code}",
            "affiliate_url": affiliate_url,
            "product_name": product_name,
        }

    async def track_click(self, short_code: str, user_id: str = None,
                          ip_hash: str = "", user_agent: str = "", referrer: str = "") -> Optional[str]:
        """Track a click and return the affiliate URL to redirect to."""
        async with self.db.acquire() as conn:
            link = await conn.fetchrow(
                "SELECT * FROM affiliate_links WHERE short_code = $1", short_code
            )
            if not link:
                return None

            await conn.execute(
                """INSERT INTO affiliate_clicks (link_id, user_id, ip_hash, user_agent, referrer)
                   VALUES ($1, $2, $3, $4, $5)""",
                link["id"], user_id, ip_hash, user_agent, referrer
            )
            return link["affiliate_url"]

    async def record_conversion(self, short_code: str, order_id: str,
                                amount_cents: int, commission_cents: int,
                                user_id: str = None) -> Dict:
        async with self.db.acquire() as conn:
            link = await conn.fetchrow(
                "SELECT id FROM affiliate_links WHERE short_code = $1", short_code
            )
            if not link:
                return {"error": "Link not found"}

            await conn.execute(
                """INSERT INTO affiliate_conversions (link_id, user_id, order_id, amount_cents, commission_cents)
                   VALUES ($1, $2, $3, $4, $5)""",
                link["id"], user_id, order_id, amount_cents, commission_cents
            )
            return {"success": True}

    async def get_stats(self, days: int = 30) -> Dict:
        async with self.db.acquire() as conn:
            clicks = await conn.fetchval(
                "SELECT COUNT(*) FROM affiliate_clicks WHERE clicked_at > NOW() - INTERVAL '%s days'" % days
            )
            conversions = await conn.fetchval(
                "SELECT COUNT(*) FROM affiliate_conversions WHERE converted_at > NOW() - INTERVAL '%s days'" % days
            )
            revenue = await conn.fetchval(
                "SELECT COALESCE(SUM(commission_cents), 0) FROM affiliate_conversions WHERE converted_at > NOW() - INTERVAL '%s days'" % days
            )
            top_links = await conn.fetch(
                """SELECT al.product_name, al.short_code, COUNT(ac.id) as click_count
                   FROM affiliate_links al
                   LEFT JOIN affiliate_clicks ac ON ac.link_id = al.id
                   WHERE ac.clicked_at > NOW() - INTERVAL '%s days'
                   GROUP BY al.id ORDER BY click_count DESC LIMIT 10""" % days
            )

        return {
            "period_days": days,
            "total_clicks": clicks,
            "total_conversions": conversions,
            "conversion_rate": round(conversions / max(clicks, 1) * 100, 2),
            "total_commission_cents": revenue,
            "top_links": [dict(r) for r in top_links],
        }

    def auto_linkify_text(self, text: str, product_links: Dict[str, str]) -> str:
        """Auto-replace product mentions in text with affiliate links."""
        for product_name, affiliate_url in product_links.items():
            pattern = re.compile(re.escape(product_name), re.IGNORECASE)
            replacement = f'<a href="{affiliate_url}" target="_blank" rel="noopener sponsored">{product_name}</a>'
            text = pattern.sub(replacement, text, count=1)
        return text
