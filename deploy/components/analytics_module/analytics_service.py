"""Analytics Service — Event tracking, usage metrics, dashboard data."""
import uuid
from typing import Optional, Dict, List
from datetime import datetime, timezone

ANALYTICS_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    page_url TEXT,
    session_id VARCHAR(100),
    ip_hash VARCHAR(64),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics_daily (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC NOT NULL DEFAULT 0,
    dimensions JSONB DEFAULT '{}',
    UNIQUE(date, metric_name, dimensions)
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_events_user ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_created ON analytics_events(created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_daily_date ON analytics_daily(date, metric_name);
"""


class AnalyticsService:
    def __init__(self, db_pool):
        self.db = db_pool

    async def track_event(self, event_type: str, user_id: str = None,
                          event_data: dict = None, page_url: str = "",
                          session_id: str = "", ip_hash: str = "", user_agent: str = ""):
        async with self.db.acquire() as conn:
            await conn.execute(
                """INSERT INTO analytics_events
                   (user_id, event_type, event_data, page_url, session_id, ip_hash, user_agent)
                   VALUES ($1, $2, $3::jsonb, $4, $5, $6, $7)""",
                user_id, event_type,
                __import__("json").dumps(event_data or {}),
                page_url, session_id, ip_hash, user_agent
            )

    async def get_dashboard_data(self, days: int = 30) -> Dict:
        async with self.db.acquire() as conn:
            total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
            active_users = await conn.fetchval(
                "SELECT COUNT(DISTINCT user_id) FROM analytics_events WHERE created_at > NOW() - INTERVAL '%s days'" % days
            )
            total_events = await conn.fetchval(
                "SELECT COUNT(*) FROM analytics_events WHERE created_at > NOW() - INTERVAL '%s days'" % days
            )
            top_events = await conn.fetch(
                """SELECT event_type, COUNT(*) as count
                   FROM analytics_events WHERE created_at > NOW() - INTERVAL '%s days'
                   GROUP BY event_type ORDER BY count DESC LIMIT 10""" % days
            )
            daily_active = await conn.fetch(
                """SELECT DATE(created_at) as date, COUNT(DISTINCT user_id) as users
                   FROM analytics_events WHERE created_at > NOW() - INTERVAL '%s days'
                   GROUP BY DATE(created_at) ORDER BY date""" % days
            )
            revenue = await conn.fetchval(
                """SELECT COALESCE(SUM(commission_cents), 0) FROM affiliate_conversions
                   WHERE converted_at > NOW() - INTERVAL '%s days'""" % days
            ) or 0
            sub_breakdown = await conn.fetch(
                "SELECT tier, COUNT(*) as count FROM subscriptions GROUP BY tier"
            )

        return {
            "total_users": total_users,
            "active_users_period": active_users,
            "total_events_period": total_events,
            "top_events": [dict(r) for r in top_events],
            "daily_active_users": [{"date": str(r["date"]), "users": r["users"]} for r in daily_active],
            "affiliate_revenue_cents": revenue,
            "subscription_breakdown": [dict(r) for r in sub_breakdown],
        }

    async def get_user_activity(self, user_id: str, limit: int = 50) -> List[Dict]:
        async with self.db.acquire() as conn:
            events = await conn.fetch(
                """SELECT event_type, event_data, page_url, created_at
                   FROM analytics_events WHERE user_id = $1
                   ORDER BY created_at DESC LIMIT $2""",
                user_id, limit
            )
        return [dict(r) for r in events]
