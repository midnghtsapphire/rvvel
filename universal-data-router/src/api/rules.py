"""
Rules API - Auto-sort and routing rules management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..models.database import AutoSortRule, RoutingRule
from ..utils.database import get_db
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Pydantic schemas
class AutoSortRuleCreate(BaseModel):
    name: str
    conditions: dict
    actions: dict
    priority: int = 0

class AutoSortRuleResponse(BaseModel):
    id: int
    name: str
    conditions: dict
    actions: dict
    is_active: bool
    priority: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoutingRuleCreate(BaseModel):
    name: str
    conditions: dict
    destination_ids: List[int]

class RoutingRuleResponse(BaseModel):
    id: int
    name: str
    conditions: dict
    destination_ids: List[int]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auto-sort rules
@router.get("/auto-sort", response_model=List[AutoSortRuleResponse])
async def list_auto_sort_rules(db: Session = Depends(get_db)):
    """
    List all auto-sort rules
    """
    rules = db.query(AutoSortRule).order_by(AutoSortRule.priority.desc()).all()
    return [AutoSortRuleResponse.from_orm(rule) for rule in rules]

@router.post("/auto-sort", response_model=AutoSortRuleResponse)
async def create_auto_sort_rule(rule: AutoSortRuleCreate, db: Session = Depends(get_db)):
    """
    Create a new auto-sort rule
    """
    new_rule = AutoSortRule(
        user_id=1,  # TODO: Get from auth context
        name=rule.name,
        conditions=rule.conditions,
        actions=rule.actions,
        priority=rule.priority
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    
    logger.info(f"Created auto-sort rule: {rule.name}")
    return AutoSortRuleResponse.from_orm(new_rule)

@router.put("/auto-sort/{rule_id}", response_model=AutoSortRuleResponse)
async def update_auto_sort_rule(
    rule_id: int,
    rule: AutoSortRuleCreate,
    db: Session = Depends(get_db)
):
    """
    Update an auto-sort rule
    """
    existing_rule = db.query(AutoSortRule).filter(AutoSortRule.id == rule_id).first()
    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    existing_rule.name = rule.name
    existing_rule.conditions = rule.conditions
    existing_rule.actions = rule.actions
    existing_rule.priority = rule.priority
    
    db.commit()
    db.refresh(existing_rule)
    
    logger.info(f"Updated auto-sort rule {rule_id}")
    return AutoSortRuleResponse.from_orm(existing_rule)

@router.delete("/auto-sort/{rule_id}")
async def delete_auto_sort_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete an auto-sort rule
    """
    rule = db.query(AutoSortRule).filter(AutoSortRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    db.delete(rule)
    db.commit()
    
    logger.info(f"Deleted auto-sort rule {rule_id}")
    return {"deleted": True}

# Routing rules
@router.get("/routing", response_model=List[RoutingRuleResponse])
async def list_routing_rules(db: Session = Depends(get_db)):
    """
    List all routing rules
    """
    rules = db.query(RoutingRule).all()
    return [RoutingRuleResponse.from_orm(rule) for rule in rules]

@router.post("/routing", response_model=RoutingRuleResponse)
async def create_routing_rule(rule: RoutingRuleCreate, db: Session = Depends(get_db)):
    """
    Create a new routing rule
    """
    new_rule = RoutingRule(
        user_id=1,  # TODO: Get from auth context
        name=rule.name,
        conditions=rule.conditions,
        destination_ids=rule.destination_ids
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    
    logger.info(f"Created routing rule: {rule.name}")
    return RoutingRuleResponse.from_orm(new_rule)

@router.put("/routing/{rule_id}", response_model=RoutingRuleResponse)
async def update_routing_rule(
    rule_id: int,
    rule: RoutingRuleCreate,
    db: Session = Depends(get_db)
):
    """
    Update a routing rule
    """
    existing_rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    existing_rule.name = rule.name
    existing_rule.conditions = rule.conditions
    existing_rule.destination_ids = rule.destination_ids
    
    db.commit()
    db.refresh(existing_rule)
    
    logger.info(f"Updated routing rule {rule_id}")
    return RoutingRuleResponse.from_orm(existing_rule)

@router.delete("/routing/{rule_id}")
async def delete_routing_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete a routing rule
    """
    rule = db.query(RoutingRule).filter(RoutingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    db.delete(rule)
    db.commit()
    
    logger.info(f"Deleted routing rule {rule_id}")
    return {"deleted": True}
