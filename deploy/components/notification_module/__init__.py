"""Reusable Notification Module — Visual-only notifications (WCAG AAA compliant, no audio)."""
from .notification_service import NotificationService
from .notification_routes import create_notification_router

__all__ = ["NotificationService", "create_notification_router"]
