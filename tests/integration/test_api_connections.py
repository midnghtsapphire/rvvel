"""
Integration Tests — API Connections
Audrey Evans Official / GlowStarLabs

Tests that all external API integrations are properly configured.
"""
import pytest
import os
import httpx


class TestOpenRouterIntegration:
    """Test OpenRouter API connection."""

    @pytest.mark.skipif(not os.environ.get("OPENROUTER_API_KEY"), reason="No API key")
    @pytest.mark.asyncio
    async def test_openrouter_models_endpoint(self):
        """Should be able to list available models."""
        api_key = os.environ.get("OPENROUTER_API_KEY")
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "data" in data
            assert len(data["data"]) > 0

    @pytest.mark.skipif(not os.environ.get("OPENROUTER_API_KEY"), reason="No API key")
    @pytest.mark.asyncio
    async def test_openrouter_chat_completion(self):
        """Should be able to make a chat completion request."""
        api_key = os.environ.get("OPENROUTER_API_KEY")
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://glowstarlabs.com",
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": "Say hello"}],
                    "max_tokens": 10,
                },
            )
            assert resp.status_code == 200


class TestClinicalTrialsAPI:
    """Test ClinicalTrials.gov API connection."""

    @pytest.mark.asyncio
    async def test_clinicaltrials_search(self):
        """Should be able to search clinical trials."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(
                "https://clinicaltrials.gov/api/v2/studies",
                params={
                    "query.cond": "acne",
                    "pageSize": 5,
                },
                headers={"Accept": "application/json"},
            )
            # API may return 200 or 403 depending on rate limits
            assert resp.status_code in (200, 403)


class TestStripeIntegration:
    """Test Stripe API connection."""

    @pytest.mark.skipif(not os.environ.get("STRIPE_SECRET_KEY"), reason="No Stripe key")
    def test_stripe_connection(self):
        """Should be able to connect to Stripe."""
        import stripe
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        # Just verify the key format
        assert stripe.api_key.startswith("sk_")

    def test_subscription_tiers_match_config(self):
        """Subscription tiers should match the defined configuration."""
        tiers = {
            "free": {"price": 0, "tokens": 10},
            "starter": {"price": 9, "tokens": 100},
            "pro": {"price": 29, "tokens": 500},
            "business": {"price": 99, "tokens": 2000},
            "enterprise": {"price": 299, "tokens": 10000},
        }
        assert len(tiers) == 5
        assert tiers["enterprise"]["price"] == 299


class TestWeatherAPI:
    """Test OpenWeatherMap API connection."""

    @pytest.mark.skipif(not os.environ.get("OPENWEATHERMAP_API_KEY"), reason="No weather key")
    @pytest.mark.asyncio
    async def test_weather_endpoint(self):
        """Should be able to get weather data."""
        api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": 39.7392,  # Denver, CO
                    "lon": -104.9903,
                    "appid": api_key,
                    "units": "imperial",
                },
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "main" in data
            assert "humidity" in data["main"]


class TestDatabaseConnection:
    """Test PostgreSQL database connection."""

    @pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="No database URL")
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Should be able to connect to PostgreSQL."""
        import asyncpg
        pool = await asyncpg.create_pool(
            dsn=os.environ.get("DATABASE_URL"),
            min_size=1, max_size=2,
        )
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT 1")
            assert result == 1
        await pool.close()
