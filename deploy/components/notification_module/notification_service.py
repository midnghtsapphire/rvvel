"""Notification Service — Visual-only notifications via WebSocket, email, push.
WCAG AAA compliant. NO audio-dependent features. Daughter is legally deaf.
All notifications are visual: banners, badges, flashing indicators, email.
"""
import json
import uuid
from typing import Optional, Dict, List, Set
from datetime import datetime, timezone
from dataclasses import dataclass
import asyncio

NOTIFICATION_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    action_url TEXT,
    icon VARCHAR(50) DEFAULT 'info',
    priority VARCHAR(20) DEFAULT 'normal',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    read_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at);
"""


@dataclass
class NotificationType:
    """Visual notification types — NO AUDIO."""
    INFO = "info"           # Blue banner, info icon
    SUCCESS = "success"     # Green banner, check icon
    WARNING = "warning"     # Amber banner, warning icon (with flash)
    ERROR = "error"         # Red banner, error icon (with flash)
    PAYMENT = "payment"     # Green banner, dollar icon
    ANALYSIS = "analysis"   # Purple banner, sparkle icon
    SYSTEM = "system"       # Gray banner, gear icon


class ConnectionManager:
    """WebSocket connection manager for real-time visual notifications."""

    def __init__(self):
        self.active_connections: Dict[str, Set] = {}  # user_id -> set of websockets

    async def connect(self, websocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            dead = set()
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.active_connections[user_id].discard(ws)

    async def broadcast(self, message: dict):
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)


class NotificationService:
    """Create and deliver visual-only notifications."""

    def __init__(self, db_pool):
        self.db = db_pool
        self.ws_manager = ConnectionManager()

    async def create_notification(
        self, user_id: str, type: str, title: str, message: str,
        action_url: str = "", icon: str = "info", priority: str = "normal"
    ) -> Dict:
        """Create a notification and push via WebSocket (visual only)."""
        notif_id = str(uuid.uuid4())

        async with self.db.acquire() as conn:
            await conn.execute(
                """INSERT INTO notifications (id, user_id, type, title, message, action_url, icon, priority)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                notif_id, user_id, type, title, message, action_url, icon, priority
            )

        notif_data = {
            "id": notif_id,
            "type": type,
            "title": title,
            "message": message,
            "action_url": action_url,
            "icon": icon,
            "priority": priority,
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            # Visual notification config — NO AUDIO
            "visual": {
                "show_banner": True,
                "flash_indicator": priority in ("high", "urgent"),
                "badge_increment": True,
                "vibrate_device": priority in ("high", "urgent"),  # Haptic only
                "persist_until_read": priority == "urgent",
            },
        }

        # Push via WebSocket
        await self.ws_manager.send_to_user(user_id, {
            "event": "notification",
            "data": notif_data,
        })

        return notif_data

    async def get_notifications(self, user_id: str, unread_only: bool = False,
                                limit: int = 50) -> List[Dict]:
        async with self.db.acquire() as conn:
            if unread_only:
                rows = await conn.fetch(
                    """SELECT * FROM notifications
                       WHERE user_id = $1 AND is_read = FALSE
                       ORDER BY created_at DESC LIMIT $2""",
                    user_id, limit
                )
            else:
                rows = await conn.fetch(
                    """SELECT * FROM notifications
                       WHERE user_id = $1
                       ORDER BY created_at DESC LIMIT $2""",
                    user_id, limit
                )
        return [dict(r) for r in rows]

    async def mark_read(self, notification_id: str, user_id: str) -> bool:
        async with self.db.acquire() as conn:
            result = await conn.execute(
                """UPDATE notifications SET is_read = TRUE, read_at = NOW()
                   WHERE id = $1 AND user_id = $2""",
                notification_id, user_id
            )
            return "UPDATE 1" in result

    async def mark_all_read(self, user_id: str) -> int:
        async with self.db.acquire() as conn:
            result = await conn.execute(
                """UPDATE notifications SET is_read = TRUE, read_at = NOW()
                   WHERE user_id = $1 AND is_read = FALSE""",
                user_id
            )
            return int(result.split()[-1]) if result else 0

    async def get_unread_count(self, user_id: str) -> int:
        async with self.db.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM notifications WHERE user_id = $1 AND is_read = FALSE",
                user_id
            )
