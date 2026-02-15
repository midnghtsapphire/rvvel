"""
Reusable Auth Module — Drop into any app
Audrey Evans Official / GlowStarLabs

Provides: Google OAuth, Apple Sign-In, Email/Password auth
JWT tokens, refresh tokens, password hashing, session management
"""
from .auth_service import AuthService, AuthConfig
from .auth_routes import create_auth_router
from .auth_models import User, UserCreate, UserLogin, TokenResponse, UserProfile

__all__ = [
    "AuthService", "AuthConfig",
    "create_auth_router",
    "User", "UserCreate", "UserLogin", "TokenResponse", "UserProfile",
]
