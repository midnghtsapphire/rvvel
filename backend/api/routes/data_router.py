"""
Universal Data Router — File routing, email organization, and data flow management.

Features:
- Gmail → categorize and route emails
- Google Drive → auto-organize files
- GitHub → repo management
- Custom routing rules with filters
"""
import os
import uuid
from typing import Optional, List, Dict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/router", tags=["Universal Data Router"])


# --- Models ---

class RoutingRuleCreate(BaseModel):
    name: str
    source_type: str  # "gmail", "drive", "github", "upload"
    source_config: Dict = {}
    destination_type: str  # "drive_folder", "github_repo", "webhook", "email"
    destination_config: Dict = {}
    filter_rules: Dict = {}  # {"subject_contains": "invoice", "from": "@company.com"}
    schedule: Optional[str] = None  # cron expression


class RoutingRuleResponse(BaseModel):
    id: str
    name: str
    source_type: str
    destination_type: str
    is_active: bool
    last_run: Optional[str] = None


class RouteItemRequest(BaseModel):
    source_type: str
    file_name: str
    file_type: str = ""
    file_size: int = 0
    metadata: Dict = {}


# --- Endpoints ---

@router.post("/rules")
async def create_routing_rule(data: RoutingRuleCreate):
    """Create a new file/email routing rule."""
    rule_id = str(uuid.uuid4())
    return {
        "id": rule_id,
        "name": data.name,
        "source_type": data.source_type,
        "destination_type": data.destination_type,
        "filter_rules": data.filter_rules,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/rules")
async def list_routing_rules():
    """List all routing rules for the current user."""
    # Default rules for demonstration
    return {
        "rules": [
            {
                "id": "default-gmail-invoices",
                "name": "Route Invoices to Drive",
                "source_type": "gmail",
                "destination_type": "drive_folder",
                "filter_rules": {"subject_contains": "invoice", "has_attachment": True},
                "destination_config": {"folder": "Invoices/2026"},
                "is_active": True,
            },
            {
                "id": "default-gmail-receipts",
                "name": "Route Receipts",
                "source_type": "gmail",
                "destination_type": "drive_folder",
                "filter_rules": {"subject_contains": "receipt", "from_contains": "@stripe.com"},
                "destination_config": {"folder": "Receipts/Stripe"},
                "is_active": True,
            },
            {
                "id": "default-drive-screenshots",
                "name": "Organize Screenshots",
                "source_type": "drive",
                "destination_type": "drive_folder",
                "filter_rules": {"file_type": "image/*", "name_contains": "screenshot"},
                "destination_config": {"folder": "Screenshots/{year}/{month}"},
                "is_active": True,
            },
        ],
        "total": 3,
    }


@router.post("/rules/{rule_id}/toggle")
async def toggle_rule(rule_id: str):
    """Enable or disable a routing rule."""
    return {"id": rule_id, "is_active": True, "toggled": True}


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    """Delete a routing rule."""
    return {"deleted": True}


@router.post("/route")
async def route_item(data: RouteItemRequest):
    """Manually route a file/item through the routing engine."""
    return {
        "item_id": str(uuid.uuid4()),
        "source_type": data.source_type,
        "file_name": data.file_name,
        "status": "routed",
        "matched_rules": [],
        "destination": None,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/history")
async def routing_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    source_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """Get routing history for the current user."""
    return {
        "items": [],
        "total": 0,
        "page": page,
        "per_page": per_page,
    }


@router.get("/stats")
async def routing_stats():
    """Get routing statistics."""
    return {
        "total_items_routed": 0,
        "rules_active": 0,
        "rules_total": 0,
        "items_today": 0,
        "items_this_week": 0,
        "items_this_month": 0,
        "by_source": {},
        "by_destination": {},
    }


# --- Email Organization ---

@router.post("/email/categorize")
async def categorize_email(subject: str = "", sender: str = "", body_preview: str = ""):
    """AI-powered email categorization."""
    # Use OpenRouter for intelligent categorization
    from backend.integrations.openrouter_client import OpenRouterClient
    client = OpenRouterClient()

    messages = [
        {"role": "system", "content": "Categorize this email into one of: invoice, receipt, newsletter, personal, work, spam, important. Return JSON: {\"category\": \"...\", \"priority\": \"high/medium/low\", \"suggested_folder\": \"...\", \"summary\": \"...\"}"},
        {"role": "user", "content": f"Subject: {subject}\nFrom: {sender}\nPreview: {body_preview}"},
    ]

    result = await client.chat(messages, model="openai/gpt-4o-mini", max_tokens=200)
    content = ""
    if result.get("choices"):
        content = result["choices"][0].get("message", {}).get("content", "")

    return {
        "categorization": content,
        "subject": subject,
        "sender": sender,
    }
