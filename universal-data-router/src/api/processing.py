"""
Processing API - Bulk, real-time, and date-range processing modes
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..models.database import InReviewItem, AutoSortRule
from ..utils.database import get_db
from ..utils.logger import setup_logger
from ..services.auto_sort import apply_auto_sort_rules

logger = setup_logger(__name__)
router = APIRouter()

class ProcessingRequest(BaseModel):
    mode: str  # 'bulk', 'real_time', 'date_range'
    params: Optional[dict] = None

@router.post("/run")
async def run_processing(
    request: ProcessingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger a processing run based on mode
    """
    if request.mode == "bulk":
        # Process all items
        items = db.query(InReviewItem).filter(InReviewItem.processed_at.is_(None)).all()
        logger.info(f"Bulk processing {len(items)} items")
        
        for item in items:
            background_tasks.add_task(apply_auto_sort_rules, item.id, db)
        
        return {"status": "queued", "items": len(items)}
    
    elif request.mode == "date_range":
        # Process items in date range
        start_date = request.params.get("start_date")
        end_date = request.params.get("end_date")
        
        query = db.query(InReviewItem).filter(InReviewItem.processed_at.is_(None))
        if start_date:
            query = query.filter(InReviewItem.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InReviewItem.created_at <= datetime.fromisoformat(end_date))
        
        items = query.all()
        logger.info(f"Date range processing {len(items)} items")
        
        for item in items:
            background_tasks.add_task(apply_auto_sort_rules, item.id, db)
        
        return {"status": "queued", "items": len(items)}
    
    elif request.mode == "real_time":
        # Real-time mode is handled by webhooks
        return {"status": "real_time mode is always active"}
    
    else:
        return {"error": "Invalid processing mode"}

@router.post("/auto-sort/run")
async def run_auto_sort(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Trigger auto-sort for all items in InReview
    """
    items = db.query(InReviewItem).filter(InReviewItem.processed_at.is_(None)).all()
    logger.info(f"Auto-sorting {len(items)} items")
    
    for item in items:
        background_tasks.add_task(apply_auto_sort_rules, item.id, db)
    
    return {"status": "queued", "items": len(items)}

@router.post("/auto-download/run")
async def run_auto_download(db: Session = Depends(get_db)):
    """
    Trigger auto-download for all attachments
    """
    # TODO: Implement auto-download logic
    logger.info("Auto-download triggered")
    return {"status": "queued"}
