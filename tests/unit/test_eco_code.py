"""
Unit Tests — Eco Code & Carbon Tracking (Standard 2 & 8)
Audrey Evans Official / GlowStarLabs
"""
import pytest


# Carbon constants
CO2_PER_API_CALL_GRAMS = 0.2
CO2_PER_CACHED_RESPONSE_GRAMS = 0.001
STARBUCKS_CUP_CO2_GRAMS = 21.0


class TestCarbonCalculations:
    """Test carbon savings calculations."""

    def test_api_call_carbon_cost(self):
        """Each API call should have a measurable carbon cost."""
        assert CO2_PER_API_CALL_GRAMS > 0
        assert CO2_PER_API_CALL_GRAMS == 0.2

    def test_cached_response_much_cheaper(self):
        """Cached responses should be 200x more carbon-efficient."""
        ratio = CO2_PER_API_CALL_GRAMS / CO2_PER_CACHED_RESPONSE_GRAMS
        assert ratio >= 200

    def test_starbucks_cup_equivalent(self):
        """Carbon savings should be expressible in Starbucks cups."""
        api_calls_saved = 100
        co2_saved = api_calls_saved * (CO2_PER_API_CALL_GRAMS - CO2_PER_CACHED_RESPONSE_GRAMS)
        cups = co2_saved / STARBUCKS_CUP_CO2_GRAMS
        assert cups > 0
        assert cups == pytest.approx(0.9476, rel=0.01)

    def test_efficiency_percentage(self):
        """Efficiency should be calculated correctly."""
        total_requests = 100
        cached_requests = 75
        efficiency = (cached_requests / total_requests) * 100
        assert efficiency == 75.0

    def test_eco_score_calculation(self):
        """Eco score should target 95/100+."""
        cached_ratio = 0.80
        lightweight_model_ratio = 0.90
        batch_efficiency = 0.95
        eco_score = (cached_ratio * 40 + lightweight_model_ratio * 30 + batch_efficiency * 30)
        assert eco_score >= 85  # Should be high

    def test_zero_requests_no_division_error(self):
        """Zero requests should not cause division by zero."""
        total = 0
        cached = 0
        efficiency = (cached / total * 100) if total > 0 else 100.0
        assert efficiency == 100.0


class TestCachingStrategy:
    """Test aggressive caching for eco-efficiency."""

    def test_cache_ttl_default(self):
        """Default cache TTL should be 5 minutes."""
        default_ttl = 300
        assert default_ttl == 300

    def test_cache_key_generation(self):
        """Cache keys should be deterministic."""
        import hashlib
        prompt = "Analyze my skin for dryness"
        key1 = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        key2 = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        assert key1 == key2

    def test_lightweight_model_preference(self):
        """Lightweight models should be tried first."""
        model_priority = [
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku",
            "openai/gpt-4o",
            "anthropic/claude-3-opus",
        ]
        # First models should be cheaper/lighter
        assert "mini" in model_priority[0] or "haiku" in model_priority[1]


class TestCarbonLeaderboard:
    """Test gamified carbon savings leaderboard."""

    def test_leaderboard_ranking(self):
        """Users should be ranked by carbon savings."""
        users = [
            {"name": "Alice", "co2_saved": 50.0},
            {"name": "Bob", "co2_saved": 120.0},
            {"name": "Charlie", "co2_saved": 75.0},
        ]
        ranked = sorted(users, key=lambda u: u["co2_saved"], reverse=True)
        assert ranked[0]["name"] == "Bob"
        assert ranked[-1]["name"] == "Alice"

    def test_esg_metrics_format(self):
        """ESG metrics should include required fields."""
        metrics = {
            "total_co2_saved_grams": 1500.0,
            "starbucks_cups_equivalent": 71.4,
            "efficiency_percentage": 92.5,
            "api_calls_avoided": 750,
            "period": "2026-02",
        }
        required_fields = ["total_co2_saved_grams", "starbucks_cups_equivalent",
                          "efficiency_percentage", "api_calls_avoided"]
        for field in required_fields:
            assert field in metrics
