"""Payment Routes — FastAPI router for Stripe payments, subscriptions, billing."""
from fastapi import APIRouter, HTTPException, Request, Depends
from .payment_models import CreateCheckoutRequest, CreateAdCheckoutRequest, SubscriptionTier, TIER_CONFIG
from .payment_service import PaymentService


AD_TIER_PRICES = {
    "basic": 2000, "standard": 5000, "premium": 10000,
    "featured": 20000, "spotlight": 50000, "exclusive": 100000, "domination": 200000,
}


def create_payment_router(payment_service: PaymentService, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/api/payments", tags=["Payments"])

    @router.get("/tiers")
    async def list_tiers():
        """List all subscription tiers and pricing."""
        return {
            tier.value: {
                "name": info["name"],
                "price_monthly": info["price"] / 100,
                "tokens": info["tokens"],
            }
            for tier, info in TIER_CONFIG.items()
        }

    @router.get("/ad-tiers")
    async def list_ad_tiers():
        """List all advertising tier pricing."""
        return {k: v / 100 for k, v in AD_TIER_PRICES.items()}

    @router.post("/checkout")
    async def create_checkout(data: CreateCheckoutRequest, user=Depends(get_current_user)):
        """Create a Stripe checkout session for subscription."""
        result = await payment_service.create_checkout_session(
            user["id"], user["email"], data.tier, data.success_url, data.cancel_url
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.post("/ad-checkout")
    async def create_ad_checkout(data: CreateAdCheckoutRequest, user=Depends(get_current_user)):
        """Create a Stripe checkout for ad space purchase."""
        if data.ad_tier not in AD_TIER_PRICES:
            raise HTTPException(status_code=400, detail=f"Invalid ad tier: {data.ad_tier}")
        amount = AD_TIER_PRICES[data.ad_tier]
        result = await payment_service.create_ad_checkout(
            user["id"], user["email"], data.ad_tier, amount,
            data.duration_days, data.success_url, data.cancel_url
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.get("/subscription")
    async def get_subscription(user=Depends(get_current_user)):
        """Get current user's subscription status."""
        sub = await payment_service.get_subscription(user["id"])
        if not sub:
            return {"tier": "free", "tokens_remaining": 10, "status": "active"}
        return sub

    @router.post("/tokens/use")
    async def use_tokens(amount: int = 1, user=Depends(get_current_user)):
        """Consume tokens for AI feature usage."""
        result = await payment_service.use_tokens(user["id"], amount)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 400), detail=result["error"])
        return result

    @router.post("/portal")
    async def billing_portal(user=Depends(get_current_user)):
        """Create Stripe billing portal session for self-service management."""
        result = await payment_service.create_portal_session(user["id"])
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.post("/cancel")
    async def cancel_subscription(user=Depends(get_current_user)):
        """Cancel subscription at end of billing period."""
        result = await payment_service.cancel_subscription(user["id"])
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.post("/webhook")
    async def stripe_webhook(request: Request):
        """Handle Stripe webhook events."""
        payload = await request.body()
        sig = request.headers.get("stripe-signature", "")
        result = await payment_service.handle_webhook(payload, sig)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 400), detail=result["error"])
        return result

    return router
