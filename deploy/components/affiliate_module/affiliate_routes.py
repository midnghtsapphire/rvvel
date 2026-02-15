"""Affiliate Routes — Track clicks, manage links, view analytics."""
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, List
import hashlib

from .affiliate_service import AffiliateService


class CreateLinkRequest(BaseModel):
    product_name: str
    original_url: str
    category: str = ""
    source_module: str = ""
    asin: str = ""


class AutoLinkRequest(BaseModel):
    text: str
    product_links: dict  # {product_name: url}


def create_affiliate_router(affiliate_service: AffiliateService, get_current_user) -> APIRouter:
    router = APIRouter(tags=["Affiliates"])

    @router.post("/api/affiliates/links")
    async def create_link(data: CreateLinkRequest, user=Depends(get_current_user)):
        """Create a new tracked affiliate link."""
        result = await affiliate_service.create_tracked_link(
            data.product_name, data.original_url,
            data.category, data.source_module, data.asin
        )
        return result

    @router.get("/go/{short_code}")
    async def redirect_affiliate(short_code: str, request: Request):
        """Track click and redirect to affiliate URL."""
        ip_hash = hashlib.sha256(
            (request.client.host or "unknown").encode()
        ).hexdigest()[:16]
        user_agent = request.headers.get("user-agent", "")
        referrer = request.headers.get("referer", "")

        url = await affiliate_service.track_click(
            short_code, ip_hash=ip_hash,
            user_agent=user_agent, referrer=referrer
        )
        if not url:
            raise HTTPException(status_code=404, detail="Link not found")
        return RedirectResponse(url=url, status_code=302)

    @router.get("/api/affiliates/stats")
    async def get_stats(days: int = 30, user=Depends(get_current_user)):
        """Get affiliate performance statistics."""
        return await affiliate_service.get_stats(days)

    @router.post("/api/affiliates/auto-link")
    async def auto_link_text(data: AutoLinkRequest, user=Depends(get_current_user)):
        """Auto-replace product mentions with affiliate links."""
        result = affiliate_service.auto_linkify_text(data.text, data.product_links)
        return {"linked_text": result}

    @router.post("/api/affiliates/amazon-search")
    async def amazon_search_link(product_name: str, user=Depends(get_current_user)):
        """Generate Amazon search affiliate link."""
        url = affiliate_service.generate_amazon_search_link(product_name)
        return {"affiliate_url": url, "product_name": product_name}

    return router
