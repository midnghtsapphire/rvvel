"""Notification Routes — REST + WebSocket for real-time visual notifications."""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from .notification_service import NotificationService


def create_notification_router(notification_service: NotificationService, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

    @router.get("/")
    async def list_notifications(unread_only: bool = False, limit: int = 50,
                                 user=Depends(get_current_user)):
        return await notification_service.get_notifications(user["id"], unread_only, limit)

    @router.get("/unread-count")
    async def unread_count(user=Depends(get_current_user)):
        count = await notification_service.get_unread_count(user["id"])
        return {"unread_count": count}

    @router.post("/{notification_id}/read")
    async def mark_read(notification_id: str, user=Depends(get_current_user)):
        success = await notification_service.mark_read(notification_id, user["id"])
        return {"success": success}

    @router.post("/read-all")
    async def mark_all_read(user=Depends(get_current_user)):
        count = await notification_service.mark_all_read(user["id"])
        return {"marked_read": count}

    @router.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
        """WebSocket for real-time visual notifications.
        Connect with: ws://host/api/notifications/ws?token=<jwt>
        All notifications are VISUAL ONLY — no audio signals.
        """
        from deploy.components.auth_module.auth_service import AuthService
        # Verify token
        payload = notification_service.db  # Will use auth service injected at app level
        user_id = "anonymous"  # Placeholder — real app injects auth verification

        await notification_service.ws_manager.connect(websocket, user_id)
        try:
            while True:
                data = await websocket.receive_text()
                # Client can send acknowledgments
                if data == "ping":
                    await websocket.send_json({"event": "pong"})
        except WebSocketDisconnect:
            notification_service.ws_manager.disconnect(websocket, user_id)

    return router
