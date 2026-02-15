"""
Destinations API - Destination configuration
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db

router = APIRouter()

@router.get("/")
async def list_destinations(db: Session = Depends(get_db)):
    """List all configured destinations"""
    return {"destinations": []}

@router.post("/")
async def create_destination(db: Session = Depends(get_db)):
    """Create a new destination"""
    return {"created": True}
