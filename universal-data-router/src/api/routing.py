"""
Routing API - Multi-destination routing and export
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..models.database import RoutingJob, InReviewItem, DestinationConfig, JobStatus
from ..utils.database import get_db
from ..utils.logger import setup_logger
from ..services.router import route_to_destinations

logger = setup_logger(__name__)
router = APIRouter()

# Pydantic schemas
class CreateRoutingJobRequest(BaseModel):
    item_ids: List[int]
    destination_ids: List[int]

class RoutingJobResponse(BaseModel):
    id: int
    item_id: int
    destination_ids: List[int]
    status: str
    results: Optional[dict]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ExportRequest(BaseModel):
    type: str  # 'individual', 'bulk', 'date_range', 'category', 'source', 'all'
    value: Optional[str] = None  # Category name, source ID, etc.
    destination_ids: List[int]
    item_ids: Optional[List[int]] = None  # For individual/bulk
    start_date: Optional[datetime] = None  # For date_range
    end_date: Optional[datetime] = None  # For date_range

@router.post("/jobs", response_model=RoutingJobResponse)
async def create_routing_job(
    request: CreateRoutingJobRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a multi-destination routing job
    """
    # Validate items exist
    items = db.query(InReviewItem).filter(InReviewItem.id.in_(request.item_ids)).all()
    if len(items) != len(request.item_ids):
        raise HTTPException(status_code=404, detail="One or more items not found")
    
    # Validate destinations exist
    destinations = db.query(DestinationConfig).filter(
        DestinationConfig.id.in_(request.destination_ids)
    ).all()
    if len(destinations) != len(request.destination_ids):
        raise HTTPException(status_code=404, detail="One or more destinations not found")
    
    # Create routing jobs for each item
    jobs = []
    for item_id in request.item_ids:
        job = RoutingJob(
            item_id=item_id,
            destination_ids=request.destination_ids,
            status=JobStatus.PENDING
        )
        db.add(job)
        db.flush()
        jobs.append(job)
        
        # Queue background task
        background_tasks.add_task(route_to_destinations, job.id, db)
    
    db.commit()
    
    logger.info(f"Created {len(jobs)} routing jobs")
    return RoutingJobResponse.from_orm(jobs[0]) if jobs else None

@router.get("/jobs/{job_id}", response_model=RoutingJobResponse)
async def get_routing_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get routing job status
    """
    job = db.query(RoutingJob).filter(RoutingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return RoutingJobResponse.from_orm(job)

@router.get("/jobs", response_model=List[RoutingJobResponse])
async def list_routing_jobs(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List routing jobs with pagination
    """
    jobs = db.query(RoutingJob).order_by(RoutingJob.created_at.desc()).offset(offset).limit(limit).all()
    return [RoutingJobResponse.from_orm(job) for job in jobs]

@router.post("/export")
async def export_items(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Flexible export endpoint for various export methods
    """
    items_to_export = []
    
    if request.type == "individual" and request.item_ids:
        items_to_export = db.query(InReviewItem).filter(InReviewItem.id.in_(request.item_ids)).all()
    
    elif request.type == "bulk" and request.item_ids:
        items_to_export = db.query(InReviewItem).filter(InReviewItem.id.in_(request.item_ids)).all()
    
    elif request.type == "date_range":
        query = db.query(InReviewItem)
        if request.start_date:
            query = query.filter(InReviewItem.created_at >= request.start_date)
        if request.end_date:
            query = query.filter(InReviewItem.created_at <= request.end_date)
        items_to_export = query.all()
    
    elif request.type == "category" and request.value:
        items_to_export = db.query(InReviewItem).filter(InReviewItem.category == request.value).all()
    
    elif request.type == "source" and request.value:
        items_to_export = db.query(InReviewItem).filter(InReviewItem.source_id == int(request.value)).all()
    
    elif request.type == "all":
        items_to_export = db.query(InReviewItem).all()
    
    else:
        raise HTTPException(status_code=400, detail="Invalid export type or missing parameters")
    
    if not items_to_export:
        raise HTTPException(status_code=404, detail="No items found for export")
    
    # Create routing jobs
    item_ids = [item.id for item in items_to_export]
    job_request = CreateRoutingJobRequest(item_ids=item_ids, destination_ids=request.destination_ids)
    
    return await create_routing_job(job_request, background_tasks, db)
