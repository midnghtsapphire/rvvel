"""Auth Models — Pydantic schemas and SQLAlchemy ORM models for authentication."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    APPLE = "apple"


class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(None, min_length=8)
    display_name: str = Field(..., min_length=1, max_length=100)
    provider: AuthProvider = AuthProvider.EMAIL
    provider_id: Optional[str] = None
    avatar_url: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    id: str
    email: str
    display_name: str
    avatar_url: Optional[str] = None
    provider: AuthProvider
    subscription_tier: str = "free"
    tokens_remaining: int = 10
    created_at: datetime
    is_active: bool = True
    roles: List[str] = ["user"]


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    user: UserProfile


class TokenRefresh(BaseModel):
    refresh_token: str


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class GoogleAuthRequest(BaseModel):
    credential: str  # Google ID token


class AppleAuthRequest(BaseModel):
    id_token: str
    authorization_code: str
    user: Optional[dict] = None  # First-time only


# SQLAlchemy table definition (as raw SQL for migrations)
USER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    provider VARCHAR(20) NOT NULL DEFAULT 'email',
    provider_id VARCHAR(255),
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
    tokens_remaining INTEGER NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    roles TEXT[] NOT NULL DEFAULT ARRAY['user'],
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_provider ON users(provider, provider_id);
"""

User = UserProfile  # Alias for backward compat
