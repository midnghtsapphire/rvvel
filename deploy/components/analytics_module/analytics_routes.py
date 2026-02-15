"""Analytics Routes — Event tracking and dashboard endpoints."""
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Optional
import hashlib

from .analytics_service import AnalyticsService


class TrackEventRequest(BaseModel):
    event_type: str
    event_data: dict = {}
    page_url: str = ""
    session_id: str = ""


def create_analytics_router(analytics_service: AnalyticsService, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

    @router.post("/track")
    async def track_event(data: TrackEventRequest, request: Request,
                          user=Depends(get_current_user)):
        ip_hash = hashlib.sha256((request.client.host or "").encode()).hexdigest()[:16]
        await analytics_service.track_event(
            data.event_type, user["id"], data.event_data,
            data.page_url, data.session_id, ip_hash,
            request.headers.get("user-agent", "")
        )
        return {"tracked": True}

    @router.post("/track/anonymous")
    async def track_anonymous(data: TrackEventRequest, request: Request):
        ip_hash = hashlib.sha256((request.client.host or "").encode()).hexdigest()[:16]
        await analytics_service.track_event(
            data.event_type, None, data.event_data,
            data.page_url, data.session_id, ip_hash,
            request.headers.get("user-agent", "")
        )
        return {"tracked": True}

    @router.get("/dashboard")
    async def dashboard(days: int = 30, user=Depends(get_current_user)):
        if "admin" not in user.get("roles", []):
            return {"error": "Admin access required"}
        return await analytics_service.get_dashboard_data(days)

    @router.get("/user/{user_id}/activity")
    async def user_activity(user_id: str, limit: int = 50, user=Depends(get_current_user)):
        if user["id"] != user_id and "admin" not in user.get("roles", []):
            return {"error": "Access denied"}
        return await analytics_service.get_user_activity(user_id, limit)

    return router
