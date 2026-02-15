"""
Reusable Affiliate Module — Auto-generate affiliate links for any product mention
Amazon Associates integration, click tracking, conversion tracking
"""
from .affiliate_service import AffiliateService, AffiliateConfig
from .affiliate_routes import create_affiliate_router

__all__ = ["AffiliateService", "AffiliateConfig", "create_affiliate_router"]
