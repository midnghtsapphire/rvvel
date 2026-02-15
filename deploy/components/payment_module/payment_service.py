"""Payment Service — Stripe subscriptions, one-time payments, token management, webhooks."""
import os
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime, timezone

import stripe

from .payment_models import SubscriptionTier, TIER_CONFIG


@dataclass
class PaymentConfig:
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    base_url: str = "https://glowstarlabs.com"

    def __post_init__(self):
        if not self.stripe_secret_key:
            self.stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
        if not self.stripe_publishable_key:
            self.stripe_publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
        if not self.stripe_webhook_secret:
            self.stripe_webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")


class PaymentService:
    """Full Stripe integration for subscriptions and ad payments."""

    def __init__(self, db_pool, config: Optional[PaymentConfig] = None):
        self.db = db_pool
        self.config = config or PaymentConfig()
        stripe.api_key = self.config.stripe_secret_key

    # ---- Customer Management ----
    async def get_or_create_customer(self, user_id: str, email: str, name: str = "") -> str:
        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT stripe_customer_id FROM subscriptions WHERE user_id = $1", user_id
            )
            if sub and sub["stripe_customer_id"]:
                return sub["stripe_customer_id"]

        customer = stripe.Customer.create(email=email, name=name, metadata={"user_id": user_id})

        async with self.db.acquire() as conn:
            await conn.execute(
                """INSERT INTO subscriptions (user_id, stripe_customer_id)
                   VALUES ($1, $2)
                   ON CONFLICT (user_id) DO UPDATE SET stripe_customer_id = $2""",
                user_id, customer.id
            )
        return customer.id

    # ---- Subscription Checkout ----
    async def create_checkout_session(
        self, user_id: str, email: str, tier: SubscriptionTier,
        success_url: str, cancel_url: str
    ) -> Dict:
        if tier == SubscriptionTier.FREE:
            return {"error": "Cannot checkout free tier"}

        customer_id = await self.get_or_create_customer(user_id, email)
        tier_info = TIER_CONFIG[tier]

        # Create or get Stripe Price
        price = self._get_or_create_price(tier)

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price.id, "quantity": 1}],
            mode="subscription",
            success_url=f"{self.config.base_url}{success_url}",
            cancel_url=f"{self.config.base_url}{cancel_url}",
            metadata={"user_id": user_id, "tier": tier.value},
            subscription_data={"metadata": {"user_id": user_id, "tier": tier.value}},
        )

        return {"checkout_url": session.url, "session_id": session.id}

    # ---- Ad Space Checkout ----
    async def create_ad_checkout(
        self, user_id: str, email: str, ad_tier: str,
        amount_cents: int, duration_days: int,
        success_url: str, cancel_url: str
    ) -> Dict:
        customer_id = await self.get_or_create_customer(user_id, email)

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": f"Ad Space - {ad_tier.title()} ({duration_days} days)",
                        "description": f"Advertising placement across GlowStarLabs network",
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{self.config.base_url}{success_url}",
            cancel_url=f"{self.config.base_url}{cancel_url}",
            metadata={
                "user_id": user_id,
                "type": "ad_purchase",
                "ad_tier": ad_tier,
                "duration_days": str(duration_days),
            },
        )

        return {"checkout_url": session.url, "session_id": session.id}

    # ---- Token Management ----
    async def use_tokens(self, user_id: str, amount: int = 1) -> Dict:
        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT * FROM subscriptions WHERE user_id = $1", user_id
            )
            if not sub:
                return {"error": "No subscription found", "status": 404}

            if sub["tokens_remaining"] < amount:
                return {
                    "error": "Insufficient tokens",
                    "remaining": sub["tokens_remaining"],
                    "upgrade_url": "/pricing",
                    "status": 402,
                }

            await conn.execute(
                """UPDATE subscriptions
                   SET tokens_remaining = tokens_remaining - $2,
                       tokens_used_this_period = tokens_used_this_period + $2,
                       updated_at = NOW()
                   WHERE user_id = $1""",
                user_id, amount
            )

            return {
                "success": True,
                "tokens_used": amount,
                "remaining": sub["tokens_remaining"] - amount,
            }

    async def get_subscription(self, user_id: str) -> Optional[Dict]:
        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT * FROM subscriptions WHERE user_id = $1", user_id
            )
            if not sub:
                return None
            return dict(sub)

    # ---- Webhook Handler ----
    async def handle_webhook(self, payload: bytes, sig_header: str) -> Dict:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.config.stripe_webhook_secret
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return {"error": "Invalid webhook signature", "status": 400}

        event_type = event["type"]
        data = event["data"]["object"]

        if event_type == "checkout.session.completed":
            await self._handle_checkout_completed(data)
        elif event_type == "customer.subscription.updated":
            await self._handle_subscription_updated(data)
        elif event_type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(data)
        elif event_type == "invoice.payment_succeeded":
            await self._handle_invoice_paid(data)
        elif event_type == "invoice.payment_failed":
            await self._handle_invoice_failed(data)

        return {"received": True}

    # ---- Webhook Handlers ----
    async def _handle_checkout_completed(self, session):
        user_id = session.get("metadata", {}).get("user_id")
        tier_str = session.get("metadata", {}).get("tier")
        if not user_id or not tier_str:
            return

        tier = SubscriptionTier(tier_str)
        tier_info = TIER_CONFIG[tier]

        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE subscriptions
                   SET tier = $2, stripe_subscription_id = $3,
                       tokens_remaining = $4, tokens_used_this_period = 0,
                       status = 'active', updated_at = NOW()
                   WHERE user_id = $1""",
                user_id, tier.value, session.get("subscription"), tier_info["tokens"]
            )
            await conn.execute(
                "UPDATE users SET subscription_tier = $2 WHERE id = $1",
                user_id, tier.value
            )

    async def _handle_subscription_updated(self, subscription):
        user_id = subscription.get("metadata", {}).get("user_id")
        if not user_id:
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE subscriptions
                   SET status = $2, cancel_at_period_end = $3,
                       current_period_start = to_timestamp($4),
                       current_period_end = to_timestamp($5),
                       updated_at = NOW()
                   WHERE user_id = $1""",
                user_id, subscription["status"],
                subscription.get("cancel_at_period_end", False),
                subscription.get("current_period_start"),
                subscription.get("current_period_end"),
            )

    async def _handle_subscription_deleted(self, subscription):
        user_id = subscription.get("metadata", {}).get("user_id")
        if not user_id:
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE subscriptions
                   SET tier = 'free', status = 'canceled',
                       tokens_remaining = 10, updated_at = NOW()
                   WHERE user_id = $1""",
                user_id
            )
            await conn.execute(
                "UPDATE users SET subscription_tier = 'free' WHERE id = $1", user_id
            )

    async def _handle_invoice_paid(self, invoice):
        customer_id = invoice.get("customer")
        if not customer_id:
            return

        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT * FROM subscriptions WHERE stripe_customer_id = $1", customer_id
            )
            if sub:
                tier = SubscriptionTier(sub["tier"])
                tier_info = TIER_CONFIG[tier]
                await conn.execute(
                    """UPDATE subscriptions
                       SET tokens_remaining = $2, tokens_used_this_period = 0,
                           status = 'active', updated_at = NOW()
                       WHERE stripe_customer_id = $1""",
                    customer_id, tier_info["tokens"]
                )

    async def _handle_invoice_failed(self, invoice):
        customer_id = invoice.get("customer")
        if not customer_id:
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE subscriptions SET status = 'past_due', updated_at = NOW()
                   WHERE stripe_customer_id = $1""",
                customer_id
            )

    # ---- Billing Portal ----
    async def create_portal_session(self, user_id: str) -> Dict:
        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT stripe_customer_id FROM subscriptions WHERE user_id = $1", user_id
            )
            if not sub or not sub["stripe_customer_id"]:
                return {"error": "No billing account found"}

        session = stripe.billing_portal.Session.create(
            customer=sub["stripe_customer_id"],
            return_url=f"{self.config.base_url}/dashboard",
        )
        return {"portal_url": session.url}

    # ---- Cancel Subscription ----
    async def cancel_subscription(self, user_id: str) -> Dict:
        async with self.db.acquire() as conn:
            sub = await conn.fetchrow(
                "SELECT stripe_subscription_id FROM subscriptions WHERE user_id = $1", user_id
            )
            if not sub or not sub["stripe_subscription_id"]:
                return {"error": "No active subscription"}

        stripe.Subscription.modify(
            sub["stripe_subscription_id"],
            cancel_at_period_end=True,
        )

        async with self.db.acquire() as conn:
            await conn.execute(
                """UPDATE subscriptions SET cancel_at_period_end = TRUE, updated_at = NOW()
                   WHERE user_id = $1""",
                user_id
            )

        return {"message": "Subscription will cancel at end of billing period"}

    # ---- Helpers ----
    def _get_or_create_price(self, tier: SubscriptionTier):
        tier_info = TIER_CONFIG[tier]
        products = stripe.Product.list(limit=100)
        product_name = f"GlowStarLabs - {tier_info['name']}"

        product = None
        for p in products.data:
            if p.name == product_name:
                product = p
                break

        if not product:
            product = stripe.Product.create(
                name=product_name,
                description=f"{tier_info['name']} subscription - {tier_info['tokens']} AI tokens/month",
            )

        prices = stripe.Price.list(product=product.id, active=True)
        for p in prices.data:
            if p.unit_amount == tier_info["price"] and p.recurring:
                return p

        price = stripe.Price.create(
            product=product.id,
            unit_amount=tier_info["price"],
            currency="usd",
            recurring={"interval": "month"},
        )
        return price
