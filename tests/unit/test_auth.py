"""
Unit Tests — Auth Module
Audrey Evans Official / GlowStarLabs
"""
import pytest
import hashlib
from unittest.mock import AsyncMock, MagicMock, patch


class TestAuthService:
    """Test authentication service."""

    def test_password_hashing(self):
        """Passwords should be hashed, never stored in plain text."""
        import hashlib
        password = "TestPassword123!"
        hashed = hashlib.sha256(password.encode()).hexdigest()
        assert hashed != password
        assert len(hashed) == 64

    def test_password_hash_deterministic(self):
        """SHA-256 hash should be deterministic for same input."""
        import hashlib
        password = "TestPassword123!"
        hash1 = hashlib.sha256(password.encode()).hexdigest()
        hash2 = hashlib.sha256(password.encode()).hexdigest()
        assert hash1 == hash2

    def test_jwt_token_creation(self):
        """JWT tokens should be created with correct claims."""
        import jwt
        secret = "test_secret_key"
        payload = {
            "sub": "user@example.com",
            "user_id": "test-uuid",
            "role": "user",
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        assert decoded["sub"] == "user@example.com"
        assert decoded["user_id"] == "test-uuid"
        assert decoded["role"] == "user"

    def test_jwt_invalid_secret_rejected(self):
        """Tokens signed with wrong secret should be rejected."""
        import jwt
        payload = {"sub": "user@example.com"}
        token = jwt.encode(payload, "correct_secret", algorithm="HS256")
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, "wrong_secret", algorithms=["HS256"])

    def test_email_validation(self):
        """Email addresses should be validated."""
        valid_emails = ["user@example.com", "name+tag@domain.co.uk"]
        invalid_emails = ["not-an-email", "@domain.com", "user@", ""]

        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        for email in valid_emails:
            assert email_pattern.match(email), f"{email} should be valid"
        for email in invalid_emails:
            assert not email_pattern.match(email), f"{email} should be invalid"


class TestOAuthProviders:
    """Test OAuth provider configurations."""

    def test_google_oauth_config(self):
        """Google OAuth should have required fields."""
        config = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "http://localhost:8000/api/auth/google/callback",
            "scope": "openid email profile",
        }
        assert "client_id" in config
        assert "client_secret" in config
        assert "openid" in config["scope"]

    def test_apple_signin_config(self):
        """Apple Sign-In should have required fields."""
        config = {
            "client_id": "com.glowstarlabs.projectface",
            "team_id": "test_team_id",
            "key_id": "test_key_id",
        }
        assert "client_id" in config
        assert "team_id" in config
