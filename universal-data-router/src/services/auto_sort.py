"""
Auto-sort service - Apply rules to automatically categorize and tag items
"""

from sqlalchemy.orm import Session
from datetime import datetime

from ..models.database import InReviewItem, AutoSortRule, Tag, ItemTag, CategoryType
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

async def apply_auto_sort_rules(item_id: int, db: Session):
    """
    Apply all active auto-sort rules to an item
    """
    item = db.query(InReviewItem).filter(InReviewItem.id == item_id).first()
    if not item:
        logger.error(f"Item {item_id} not found")
        return
    
    # Get all active rules ordered by priority
    rules = db.query(AutoSortRule).filter(
        AutoSortRule.is_active == True
    ).order_by(AutoSortRule.priority.desc()).all()
    
    for rule in rules:
        if matches_conditions(item, rule.conditions):
            apply_actions(item, rule.actions, db)
            logger.info(f"Applied rule '{rule.name}' to item {item_id}")
    
    # Mark as processed
    item.processed_at = datetime.utcnow()
    db.commit()

def matches_conditions(item: InReviewItem, conditions: dict) -> bool:
    """
    Check if an item matches rule conditions
    """
    # Example conditions:
    # {"from": "*@example.com", "has_attachment": true, "subject_contains": "Invoice"}
    
    metadata = item.metadata or {}
    
    # Check 'from' field
    if "from" in conditions:
        from_pattern = conditions["from"]
        email_from = metadata.get("from", "")
        if from_pattern.startswith("*@"):
            domain = from_pattern[2:]
            if not email_from.endswith(domain):
                return False
        elif from_pattern != email_from:
            return False
    
    # Check 'has_attachment'
    if "has_attachment" in conditions:
        has_attachment = len(item.attachments) > 0
        if conditions["has_attachment"] != has_attachment:
            return False
    
    # Check 'subject_contains'
    if "subject_contains" in conditions:
        subject = metadata.get("subject", "")
        if conditions["subject_contains"].lower() not in subject.lower():
            return False
    
    # Check 'category'
    if "category" in conditions:
        if item.category != CategoryType(conditions["category"]):
            return False
    
    return True

def apply_actions(item: InReviewItem, actions: dict, db: Session):
    """
    Apply rule actions to an item
    """
    # Set category
    if "set_category" in actions:
        try:
            item.category = CategoryType(actions["set_category"])
        except ValueError:
            logger.warning(f"Invalid category: {actions['set_category']}")
    
    # Add tags
    if "add_tags" in actions:
        for tag_name in actions["add_tags"]:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            
            # Check if tag already exists for this item
            existing = db.query(ItemTag).filter(
                ItemTag.item_id == item.id,
                ItemTag.tag_id == tag.id
            ).first()
            
            if not existing:
                item_tag = ItemTag(item_id=item.id, tag_id=tag.id)
                db.add(item_tag)
    
    db.flush()
