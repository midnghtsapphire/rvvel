"""Admin Dashboard Routes — User management, system health, content moderation."""
from fastapi import APIRouter, Depends, HTTPException


def require_admin(get_current_user):
    async def _check(user=Depends(get_current_user)):
        if "admin" not in user.get("roles", []):
            raise HTTPException(status_code=403, detail="Admin access required")
        return user
    return _check


def create_admin_router(db_pool, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/api/admin", tags=["Admin"])
    admin_required = require_admin(get_current_user)

    @router.get("/users")
    async def list_users(page: int = 1, per_page: int = 50, user=Depends(admin_required)):
        offset = (page - 1) * per_page
        async with db_pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM users")
            users = await conn.fetch(
                """SELECT id, email, display_name, provider, subscription_tier,
                          tokens_remaining, is_active, roles, created_at, last_login
                   FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2""",
                per_page, offset
            )
        return {"total": total, "page": page, "per_page": per_page,
                "users": [dict(u) for u in users]}

    @router.get("/users/{user_id}")
    async def get_user(user_id: str, user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            u = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
            if not u:
                raise HTTPException(status_code=404, detail="User not found")
            sub = await conn.fetchrow("SELECT * FROM subscriptions WHERE user_id = $1", user_id)
        return {"user": dict(u), "subscription": dict(sub) if sub else None}

    @router.post("/users/{user_id}/deactivate")
    async def deactivate_user(user_id: str, user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            await conn.execute("UPDATE users SET is_active = FALSE WHERE id = $1", user_id)
        return {"deactivated": True}

    @router.post("/users/{user_id}/activate")
    async def activate_user(user_id: str, user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            await conn.execute("UPDATE users SET is_active = TRUE WHERE id = $1", user_id)
        return {"activated": True}

    @router.post("/users/{user_id}/set-role")
    async def set_role(user_id: str, role: str, user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET roles = array_append(roles, $2) WHERE id = $1 AND NOT ($2 = ANY(roles))",
                user_id, role
            )
        return {"role_added": role}

    @router.get("/health")
    async def system_health(user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            db_ok = await conn.fetchval("SELECT 1")
            user_count = await conn.fetchval("SELECT COUNT(*) FROM users")
            sub_count = await conn.fetchval("SELECT COUNT(*) FROM subscriptions WHERE tier != 'free'")
            active_ads = await conn.fetchval("SELECT COUNT(*) FROM ad_placements WHERE status = 'active'")
        return {
            "status": "healthy",
            "database": "connected" if db_ok else "error",
            "total_users": user_count,
            "paid_subscribers": sub_count,
            "active_ads": active_ads,
        }

    @router.get("/revenue")
    async def revenue_summary(days: int = 30, user=Depends(admin_required)):
        async with db_pool.acquire() as conn:
            sub_revenue = await conn.fetchval(
                """SELECT COALESCE(SUM(amount_paid_cents), 0) FROM ad_placements
                   WHERE created_at > NOW() - INTERVAL '%s days'""" % days
            )
            affiliate_revenue = await conn.fetchval(
                """SELECT COALESCE(SUM(commission_cents), 0) FROM affiliate_conversions
                   WHERE converted_at > NOW() - INTERVAL '%s days'""" % days
            )
        return {
            "period_days": days,
            "ad_revenue_cents": sub_revenue or 0,
            "affiliate_revenue_cents": affiliate_revenue or 0,
            "total_revenue_cents": (sub_revenue or 0) + (affiliate_revenue or 0),
        }

    return router
