"""
Sources API - Data source configuration
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db

router = APIRouter()

@router.get("/")
async def list_sources(db: Session = Depends(get_db)):
    """List all configured sources"""
    return {"sources": []}

@router.post("/")
async def create_source(db: Session = Depends(get_db)):
    """Create a new source"""
    return {"created": True}
