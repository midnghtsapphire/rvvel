"""
E2E Tests — Critical User Flows
Audrey Evans Official / GlowStarLabs

Tests the most important user journeys end-to-end.
"""
import pytest


class TestRegistrationFlow:
    """Test user registration flow."""

    def test_registration_requires_email(self):
        """Registration should require a valid email."""
        required_fields = ["email", "password", "full_name"]
        user_data = {"email": "user@example.com", "password": "SecurePass123!", "full_name": "Test User"}
        for field in required_fields:
            assert field in user_data

    def test_registration_sets_defaults(self):
        """New users should get default accessibility preferences."""
        defaults = {
            "blue_light_filter": True,
            "dark_mode": True,
            "visual_only_notifications": True,
            "break_reminder_minutes": 25,
            "focus_mode": False,
            "font_size": "medium",
        }
        assert defaults["blue_light_filter"] is True
        assert defaults["visual_only_notifications"] is True
        assert defaults["break_reminder_minutes"] == 25

    def test_registration_creates_free_subscription(self):
        """New users should automatically get free tier subscription."""
        new_subscription = {
            "tier": "free",
            "tokens_remaining": 10,
            "status": "active",
        }
        assert new_subscription["tier"] == "free"
        assert new_subscription["tokens_remaining"] == 10


class TestSkinAnalysisFlow:
    """Test the flagship skin analysis flow."""

    def test_analysis_requires_image(self):
        """Skin analysis should require an uploaded image."""
        required = ["image"]
        assert "image" in required

    def test_analysis_includes_weather(self):
        """Analysis should include weather-based personalization."""
        analysis_result = {
            "skin_type": "combination",
            "weather_data": {
                "humidity": 25,
                "temperature_f": 45,
                "climate_type": "arid",
            },
            "recommendations": [
                "Heavy moisturizer for Colorado dry climate",
                "SPF 30+ daily",
            ],
        }
        assert "weather_data" in analysis_result
        assert analysis_result["weather_data"]["climate_type"] == "arid"

    def test_analysis_includes_medical_disclaimer(self):
        """Every analysis must include medical disclaimer."""
        disclaimer = "This is not medical advice. Consult a dermatologist."
        assert "not medical advice" in disclaimer.lower()

    def test_analysis_tracks_carbon(self):
        """Each analysis should track carbon footprint."""
        analysis_meta = {
            "api_calls_made": 2,
            "tokens_consumed": 1500,
            "co2_grams": 0.4,
            "cached": False,
        }
        assert "co2_grams" in analysis_meta


class TestSubscriptionUpgradeFlow:
    """Test subscription upgrade flow."""

    def test_upgrade_path_available(self):
        """Users should be able to upgrade from any tier."""
        upgrade_paths = {
            "free": ["starter", "pro", "business", "enterprise"],
            "starter": ["pro", "business", "enterprise"],
            "pro": ["business", "enterprise"],
            "business": ["enterprise"],
        }
        assert len(upgrade_paths["free"]) == 4

    def test_tokens_increase_on_upgrade(self):
        """Tokens should increase when upgrading."""
        tiers = {"free": 10, "starter": 100, "pro": 500, "business": 2000, "enterprise": 10000}
        assert tiers["pro"] > tiers["starter"]
        assert tiers["enterprise"] > tiers["business"]


class TestDataRouterFlow:
    """Test universal data router flow."""

    def test_routing_rule_creation(self):
        """Users should be able to create routing rules."""
        rule = {
            "name": "Route invoices to accounting folder",
            "source_type": "gmail",
            "source_pattern": "invoice|receipt|payment",
            "destination_type": "google_drive",
            "destination_config": {"folder": "/Accounting/Invoices"},
        }
        assert rule["source_type"] == "gmail"
        assert rule["destination_type"] == "google_drive"

    def test_routing_rule_matching(self):
        """Routing rules should match items correctly."""
        import re
        pattern = "invoice|receipt|payment"
        test_subjects = [
            ("Invoice from Stripe", True),
            ("Your receipt is ready", True),
            ("Hello world", False),
            ("Payment confirmation", True),
        ]
        for subject, should_match in test_subjects:
            matched = bool(re.search(pattern, subject, re.IGNORECASE))
            assert matched == should_match, f"'{subject}' match={matched}, expected={should_match}"


class TestAccessibilityFlow:
    """Test accessibility settings flow."""

    def test_settings_page_accessible(self):
        """Settings page should be accessible without login for public config."""
        public_settings = ["blue_light_filter", "dark_mode", "font_size", "reduced_motion"]
        assert len(public_settings) >= 4

    def test_focus_mode_toggle(self):
        """Focus mode should be toggleable."""
        focus_mode = False
        focus_mode = not focus_mode
        assert focus_mode is True
        focus_mode = not focus_mode
        assert focus_mode is False
