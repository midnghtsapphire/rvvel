"""Selling Space Routes — Ad management, purchasing, and serving."""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
import hashlib

from .selling_space_service import SellingSpaceService, AD_TIERS


class CreateAdRequest(BaseModel):
    title: str
    description: str = ""
    image_url: str = ""
    click_url: str
    ad_tier: str = "basic"
    placement_type: str = "sidebar"
    target_domains: List[str] = []
    duration_days: int = 30


def create_selling_space_router(selling_space_service: SellingSpaceService, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/api/ads", tags=["Selling Space"])

    @router.get("/tiers")
    async def list_tiers():
        return {k: {"price": v["price_cents"] / 100, "max_impressions": v["max_impressions"],
                     "placements": v["placement"]} for k, v in AD_TIERS.items()}

    @router.post("/create")
    async def create_ad(data: CreateAdRequest, user=Depends(get_current_user)):
        result = await selling_space_service.create_ad(
            user["id"], data.title, data.description, data.image_url,
            data.click_url, data.ad_tier, data.placement_type,
            data.target_domains, data.duration_days
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.get("/active")
    async def get_active_ads(domain: str = "", placement: str = "", limit: int = 5):
        return await selling_space_service.get_active_ads(domain, placement, limit)

    @router.get("/click/{ad_id}")
    async def click_ad(ad_id: str, request: Request):
        ip_hash = hashlib.sha256((request.client.host or "").encode()).hexdigest()[:16]
        await selling_space_service.record_click(ad_id, ip_hash, request.headers.get("user-agent", ""))
        # In production, redirect to click_url
        return {"tracked": True}

    @router.post("/impression/{ad_id}")
    async def record_impression(ad_id: str, request: Request, page_url: str = ""):
        ip_hash = hashlib.sha256((request.client.host or "").encode()).hexdigest()[:16]
        await selling_space_service.record_impression(ad_id, page_url, ip_hash)
        return {"tracked": True}

    @router.get("/my-ads")
    async def my_ads(user=Depends(get_current_user)):
        return await selling_space_service.get_advertiser_stats(user["id"])

    return router
