"""Payment Models — Subscription tiers, checkout, invoicing."""
from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime


class SubscriptionTier(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


TIER_CONFIG = {
    SubscriptionTier.FREE: {"price": 0, "tokens": 10, "name": "Free"},
    SubscriptionTier.STARTER: {"price": 900, "tokens": 100, "name": "Starter"},  # cents
    SubscriptionTier.PRO: {"price": 2900, "tokens": 500, "name": "Pro"},
    SubscriptionTier.BUSINESS: {"price": 9900, "tokens": 2000, "name": "Business"},
    SubscriptionTier.ENTERPRISE: {"price": 29900, "tokens": 10000, "name": "Enterprise"},
}


class CreateCheckoutRequest(BaseModel):
    tier: SubscriptionTier
    success_url: str = "/dashboard?payment=success"
    cancel_url: str = "/pricing?payment=cancelled"


class CreateAdCheckoutRequest(BaseModel):
    ad_tier: str  # basic, standard, premium, featured, spotlight, exclusive, domination
    duration_days: int = 30
    placement: str = "sidebar"  # sidebar, banner, featured, popup
    target_domains: List[str] = []
    success_url: str = "/ads/dashboard?payment=success"
    cancel_url: str = "/ads/pricing?payment=cancelled"


class SubscriptionStatus(BaseModel):
    user_id: str
    tier: SubscriptionTier
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    status: str = "active"  # active, past_due, canceled, trialing
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    tokens_remaining: int = 10
    tokens_used_this_period: int = 0
    cancel_at_period_end: bool = False


class InvoiceData(BaseModel):
    invoice_id: str
    user_id: str
    amount: int  # cents
    currency: str = "usd"
    status: str
    created_at: datetime
    pdf_url: Optional[str] = None


class WebhookEvent(BaseModel):
    type: str
    data: Dict


SUBSCRIPTION_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(20) NOT NULL DEFAULT 'free',
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    tokens_remaining INTEGER NOT NULL DEFAULT 10,
    tokens_used_this_period INTEGER NOT NULL DEFAULT 0,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_customer ON subscriptions(stripe_customer_id);
"""
