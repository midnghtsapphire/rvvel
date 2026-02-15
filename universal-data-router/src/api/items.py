"""
Items API - InReview staging area management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..models.database import InReviewItem, CategoryType, Tag, ItemTag
from ..utils.database import get_db
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Pydantic schemas
class ItemResponse(BaseModel):
    id: int
    source_id: Optional[int]
    category: Optional[str]
    content: Optional[str]
    metadata: Optional[dict]
    preview_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class ItemListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    limit: int
    offset: int

@router.get("/", response_model=ItemListResponse)
async def list_items(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    source_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    tags: Optional[str] = None,  # Comma-separated
    db: Session = Depends(get_db)
):
    """
    List items in InReview staging area with filtering and pagination
    """
    query = db.query(InReviewItem)
    
    # Apply filters
    if category:
        query = query.filter(InReviewItem.category == category)
    if source_id:
        query = query.filter(InReviewItem.source_id == source_id)
    if start_date:
        query = query.filter(InReviewItem.created_at >= start_date)
    if end_date:
        query = query.filter(InReviewItem.created_at <= end_date)
    if tags:
        tag_list = tags.split(',')
        query = query.join(ItemTag).join(Tag).filter(Tag.name.in_(tag_list))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    items = query.order_by(InReviewItem.created_at.desc()).offset(offset).limit(limit).all()
    
    return ItemListResponse(
        items=[ItemResponse.from_orm(item) for item in items],
        total=total,
        limit=limit,
        offset=offset
    )

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single item by ID
    """
    item = db.query(InReviewItem).filter(InReviewItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.from_orm(item)

@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, update: ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an item (category, tags, etc.)
    """
    item = db.query(InReviewItem).filter(InReviewItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update category
    if update.category:
        try:
            item.category = CategoryType(update.category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {update.category}")
    
    # Update tags
    if update.tags is not None:
        # Remove existing tags
        db.query(ItemTag).filter(ItemTag.item_id == item_id).delete()
        
        # Add new tags
        for tag_name in update.tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            
            item_tag = ItemTag(item_id=item_id, tag_id=tag.id)
            db.add(item_tag)
    
    db.commit()
    db.refresh(item)
    
    logger.info(f"Updated item {item_id}")
    return ItemResponse.from_orm(item)

@router.delete("/")
async def delete_items(item_ids: List[int], db: Session = Depends(get_db)):
    """
    Delete multiple items in bulk
    """
    deleted_count = db.query(InReviewItem).filter(InReviewItem.id.in_(item_ids)).delete(synchronize_session=False)
    db.commit()
    
    logger.info(f"Deleted {deleted_count} items")
    return {"deleted": deleted_count}

@router.get("/date-range/today")
async def get_today_items(db: Session = Depends(get_db)):
    """
    Get items from today
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    items = db.query(InReviewItem).filter(InReviewItem.created_at >= today_start).all()
    return {"items": [ItemResponse.from_orm(item) for item in items]}

@router.get("/date-range/week")
async def get_week_items(db: Session = Depends(get_db)):
    """
    Get items from this week
    """
    week_start = datetime.now() - timedelta(days=7)
    items = db.query(InReviewItem).filter(InReviewItem.created_at >= week_start).all()
    return {"items": [ItemResponse.from_orm(item) for item in items]}

@router.get("/date-range/month")
async def get_month_items(db: Session = Depends(get_db)):
    """
    Get items from this month
    """
    month_start = datetime.now() - timedelta(days=30)
    items = db.query(InReviewItem).filter(InReviewItem.created_at >= month_start).all()
    return {"items": [ItemResponse.from_orm(item) for item in items]}
