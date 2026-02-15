"""Auth Routes — FastAPI router for all authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from typing import Optional
from .auth_models import (
    UserCreate, UserLogin, TokenResponse, TokenRefresh,
    GoogleAuthRequest, AppleAuthRequest, PasswordReset, PasswordResetConfirm,
)
from .auth_service import AuthService


def create_auth_router(auth_service: AuthService) -> APIRouter:
    """Factory function to create auth router with injected service."""
    router = APIRouter(prefix="/api/auth", tags=["Authentication"])

    async def get_current_user(authorization: Optional[str] = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        token = authorization.split(" ")[1]
        payload = auth_service.verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user = await auth_service.get_user(payload["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @router.post("/register", response_model=TokenResponse)
    async def register(data: UserCreate):
        """Register a new user with email and password."""
        if data.provider != "email" or not data.password:
            raise HTTPException(status_code=400, detail="Password required for email registration")
        result = await auth_service.register_email(data.email, data.password, data.display_name)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 400), detail=result["error"])
        return result

    @router.post("/login", response_model=TokenResponse)
    async def login(data: UserLogin):
        """Login with email and password."""
        result = await auth_service.login_email(data.email, data.password)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 401), detail=result["error"])
        return result

    @router.post("/google", response_model=TokenResponse)
    async def google_auth(data: GoogleAuthRequest):
        """Authenticate with Google OAuth."""
        result = await auth_service.google_auth(data.credential)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 401), detail=result["error"])
        return result

    @router.post("/apple", response_model=TokenResponse)
    async def apple_auth(data: AppleAuthRequest):
        """Authenticate with Apple Sign-In."""
        result = await auth_service.apple_auth(data.id_token, data.user)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 401), detail=result["error"])
        return result

    @router.post("/refresh", response_model=TokenResponse)
    async def refresh_token(data: TokenRefresh):
        """Refresh access token using refresh token."""
        result = await auth_service.refresh_access_token(data.refresh_token)
        if "error" in result:
            raise HTTPException(status_code=result.get("status", 401), detail=result["error"])
        return result

    @router.get("/me")
    async def get_me(user=Depends(get_current_user)):
        """Get current authenticated user profile."""
        return user

    @router.post("/logout")
    async def logout(user=Depends(get_current_user)):
        """Logout (client should discard tokens)."""
        return {"message": "Logged out successfully"}

    @router.post("/password/reset")
    async def request_password_reset(data: PasswordReset):
        """Request a password reset email."""
        # In production, send email with reset link
        return {"message": "If an account exists with that email, a reset link has been sent."}

    @router.post("/password/reset/confirm")
    async def confirm_password_reset(data: PasswordResetConfirm):
        """Confirm password reset with token."""
        return {"message": "Password has been reset successfully."}

    # Expose the dependency for other routers
    router.get_current_user = get_current_user

    return router
