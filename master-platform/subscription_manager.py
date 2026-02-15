"""Master Platform: Subscription Manager
Token-based usage + Stripe integration for subscription tiers.
Author: Audrey Evans
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")

class SubscriptionTier(str, Enum):
    FREE = "free"
    STARTER = "starter"      # $9/mo
    PRO = "pro"              # $29/mo
    BUSINESS = "business"    # $99/mo
    ENTERPRISE = "enterprise"  # $299/mo

TIER_LIMITS = {
    SubscriptionTier.FREE: {"tokens": 10, "features": ["skin_analysis_basic"]},
    SubscriptionTier.STARTER: {"tokens": 100, "features": ["skin_analysis", "makeup_advisor"]},
    SubscriptionTier.PRO: {"tokens": 500, "features": ["all", "priority_support"]},
    SubscriptionTier.BUSINESS: {"tokens": 2000, "features": ["all", "api_access", "white_label"]},
    SubscriptionTier.ENTERPRISE: {"tokens": 10000, "features": ["all", "dedicated_support", "custom_integration"]},
}

@dataclass
class UserSubscription:
    user_id: str
    tier: SubscriptionTier
    tokens_remaining: int
    stripe_subscription_id: Optional[str] = None
    renewal_date: Optional[str] = None

class SubscriptionManager:
    def __init__(self):
        self.tiers = TIER_LIMITS
    
    def get_tier_info(self, tier: SubscriptionTier) -> Dict:
        return self.tiers.get(tier, {})
    
    def use_tokens(self, subscription: UserSubscription, amount: int) -> Dict:
        if subscription.tokens_remaining >= amount:
            subscription.tokens_remaining -= amount
            return {"success": True, "remaining": subscription.tokens_remaining}
        return {"success": False, "error": "Insufficient tokens", "upgrade_url": "/upgrade"}
    
    def create_stripe_checkout(self, tier: SubscriptionTier, user_email: str) -> Dict:
        prices = {
            SubscriptionTier.STARTER: "price_starter_9",
            SubscriptionTier.PRO: "price_pro_29",
            SubscriptionTier.BUSINESS: "price_business_99",
            SubscriptionTier.ENTERPRISE: "price_enterprise_299",
        }
        return {
            "checkout_url": f"https://checkout.stripe.com/{tier.value}",
            "price_id": prices.get(tier, ""),
            "user_email": user_email,
        }

if __name__ == "__main__":
    manager = SubscriptionManager()
    sub = UserSubscription("user123", SubscriptionTier.PRO, 500)
    result = manager.use_tokens(sub, 10)
    print(f"Tokens remaining: {result['remaining']}")
