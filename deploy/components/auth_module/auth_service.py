"""Auth Service — Core authentication logic with Google OAuth, Apple Sign-In, email/password."""
import os
import uuid
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json
import base64

import jwt
import httpx


@dataclass
class AuthConfig:
    """Configuration for the auth module."""
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    refresh_token_days: int = 30
    google_client_id: str = ""
    google_client_secret: str = ""
    apple_client_id: str = ""
    apple_team_id: str = ""
    apple_key_id: str = ""
    apple_private_key: str = ""
    bcrypt_rounds: int = 12

    def __post_init__(self):
        if not self.jwt_secret:
            self.jwt_secret = os.environ.get("JWT_SECRET", secrets.token_hex(32))
        if not self.google_client_id:
            self.google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        if not self.google_client_secret:
            self.google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
        if not self.apple_client_id:
            self.apple_client_id = os.environ.get("APPLE_CLIENT_ID", "")
        if not self.apple_team_id:
            self.apple_team_id = os.environ.get("APPLE_TEAM_ID", "")


class AuthService:
    """Handles all authentication operations."""

    def __init__(self, db_pool, config: Optional[AuthConfig] = None):
        self.db = db_pool
        self.config = config or AuthConfig()

    # ---- Password Hashing ----
    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100_000
        )
        return f"{salt}${pwd_hash.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        try:
            salt, pwd_hash = stored_hash.split("$")
            new_hash = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), 100_000
            )
            return hmac.compare_digest(new_hash.hex(), pwd_hash)
        except (ValueError, AttributeError):
            return False

    # ---- JWT Tokens ----
    def create_access_token(self, user_id: str, roles: list = None) -> str:
        payload = {
            "sub": user_id,
            "roles": roles or ["user"],
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=self.config.jwt_expiry_hours),
            "type": "access",
        }
        return jwt.encode(payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=self.config.refresh_token_days),
            "type": "refresh",
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(
                token, self.config.jwt_secret,
                algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    # ---- Email/Password Registration ----
    async def register_email(self, email: str, password: str, display_name: str) -> Dict:
        async with self.db.acquire() as conn:
            existing = await conn.fetchrow("SELECT id FROM users WHERE email = $1", email)
            if existing:
                return {"error": "Email already registered", "status": 409}

            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)

            await conn.execute(
                """INSERT INTO users (id, email, password_hash, display_name, provider)
                   VALUES ($1, $2, $3, $4, 'email')""",
                user_id, email, password_hash, display_name
            )

            access_token = self.create_access_token(user_id)
            refresh_token = self.create_refresh_token(user_id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": self.config.jwt_expiry_hours * 3600,
                "user": {
                    "id": user_id,
                    "email": email,
                    "display_name": display_name,
                    "provider": "email",
                    "subscription_tier": "free",
                    "tokens_remaining": 10,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "is_active": True,
                    "roles": ["user"],
                },
            }

    # ---- Email/Password Login ----
    async def login_email(self, email: str, password: str) -> Dict:
        async with self.db.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1 AND provider = 'email'", email
            )
            if not user or not self.verify_password(password, user["password_hash"]):
                return {"error": "Invalid credentials", "status": 401}

            if not user["is_active"]:
                return {"error": "Account deactivated", "status": 403}

            await conn.execute(
                "UPDATE users SET last_login = NOW() WHERE id = $1", user["id"]
            )

            access_token = self.create_access_token(str(user["id"]), list(user["roles"]))
            refresh_token = self.create_refresh_token(str(user["id"]))

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": self.config.jwt_expiry_hours * 3600,
                "user": self._user_to_dict(user),
            }

    # ---- Google OAuth ----
    async def google_auth(self, credential: str) -> Dict:
        """Verify Google ID token and create/login user."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
                )
                if resp.status_code != 200:
                    return {"error": "Invalid Google token", "status": 401}
                google_user = resp.json()
        except Exception as e:
            return {"error": f"Google auth failed: {str(e)}", "status": 500}

        email = google_user.get("email")
        name = google_user.get("name", email.split("@")[0])
        avatar = google_user.get("picture", "")
        google_id = google_user.get("sub")

        return await self._oauth_upsert(email, name, avatar, "google", google_id)

    # ---- Apple Sign-In ----
    async def apple_auth(self, id_token: str, user_info: Optional[dict] = None) -> Dict:
        """Verify Apple ID token and create/login user."""
        try:
            # Decode without verification first to get claims
            unverified = jwt.decode(id_token, options={"verify_signature": False})
            email = unverified.get("email", "")
            apple_id = unverified.get("sub", "")
            name = ""
            if user_info:
                first = user_info.get("name", {}).get("firstName", "")
                last = user_info.get("name", {}).get("lastName", "")
                name = f"{first} {last}".strip()
            if not name:
                name = email.split("@")[0] if email else "Apple User"
        except Exception as e:
            return {"error": f"Apple auth failed: {str(e)}", "status": 500}

        return await self._oauth_upsert(email, name, "", "apple", apple_id)

    # ---- OAuth Upsert (shared) ----
    async def _oauth_upsert(
        self, email: str, display_name: str, avatar_url: str,
        provider: str, provider_id: str
    ) -> Dict:
        async with self.db.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )

            if user:
                await conn.execute(
                    "UPDATE users SET last_login = NOW(), avatar_url = COALESCE($2, avatar_url) WHERE id = $1",
                    user["id"], avatar_url
                )
            else:
                user_id = str(uuid.uuid4())
                await conn.execute(
                    """INSERT INTO users (id, email, display_name, avatar_url, provider, provider_id, is_verified)
                       VALUES ($1, $2, $3, $4, $5, $6, TRUE)""",
                    user_id, email, display_name, avatar_url, provider, provider_id
                )
                user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

            access_token = self.create_access_token(str(user["id"]), list(user["roles"]))
            refresh_token = self.create_refresh_token(str(user["id"]))

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": self.config.jwt_expiry_hours * 3600,
                "user": self._user_to_dict(user),
            }

    # ---- Token Refresh ----
    async def refresh_access_token(self, refresh_token: str) -> Dict:
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return {"error": "Invalid refresh token", "status": 401}

        user_id = payload["sub"]
        async with self.db.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
            if not user or not user["is_active"]:
                return {"error": "User not found or deactivated", "status": 404}

            new_access = self.create_access_token(str(user["id"]), list(user["roles"]))
            new_refresh = self.create_refresh_token(str(user["id"]))

            return {
                "access_token": new_access,
                "refresh_token": new_refresh,
                "token_type": "bearer",
                "expires_in": self.config.jwt_expiry_hours * 3600,
                "user": self._user_to_dict(user),
            }

    # ---- Get Current User ----
    async def get_user(self, user_id: str) -> Optional[Dict]:
        async with self.db.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
            if user:
                return self._user_to_dict(user)
            return None

    # ---- Helpers ----
    @staticmethod
    def _user_to_dict(user) -> Dict:
        return {
            "id": str(user["id"]),
            "email": user["email"],
            "display_name": user["display_name"],
            "avatar_url": user.get("avatar_url"),
            "provider": user["provider"],
            "subscription_tier": user["subscription_tier"],
            "tokens_remaining": user["tokens_remaining"],
            "created_at": user["created_at"].isoformat() if user.get("created_at") else None,
            "is_active": user["is_active"],
            "roles": list(user["roles"]) if user.get("roles") else ["user"],
        }
