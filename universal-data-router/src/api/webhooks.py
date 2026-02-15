"""
Webhooks API - Receive data from external sources
"""

from fastapi import APIRouter, Request, BackgroundTasks
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/email/gmail")
async def gmail_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive Gmail push notifications
    """
    data = await request.json()
    logger.info(f"Received Gmail webhook: {data}")
    
    # TODO: Process email, extract attachments, auto-categorize
    
    return {"status": "received"}

@router.post("/generic")
async def generic_webhook(request: Request):
    """
    Generic webhook endpoint for other sources
    """
    data = await request.json()
    logger.info(f"Received generic webhook: {data}")
    return {"status": "received"}
