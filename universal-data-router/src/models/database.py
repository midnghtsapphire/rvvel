"""
Database models for Universal Data Router (Revvel)
SQLAlchemy ORM models with PostgreSQL support
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey,
    JSON, Float, Enum, Index, UniqueConstraint, TIMESTAMP
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import TSVECTOR, INET, JSONB
import enum

Base = declarative_base()

# Enums
class CategoryType(str, enum.Enum):
    CODE = "code"
    DOCUMENT = "document"
    IMAGE = "image"
    PROMPT = "prompt"
    LEGAL = "legal"
    MUSIC = "music"
    INVENTION = "invention"
    BUSINESS_PLAN = "business_plan"
    RESEARCH = "research"
    PERSONAL = "personal"

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class ProcessingMode(str, enum.Enum):
    BULK = "bulk"
    REAL_TIME = "real_time"
    DATE_RANGE = "date_range"

# Models
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(255))
    dark_mode = Column(Boolean, default=True)
    warm_accent = Column(Boolean, default=True)
    accessibility_mode = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = relationship("InReviewItem", back_populates="user", cascade="all, delete-orphan")
    routing_rules = relationship("RoutingRule", back_populates="user", cascade="all, delete-orphan")
    auto_sort_rules = relationship("AutoSortRule", back_populates="user", cascade="all, delete-orphan")


class SourceConfig(Base):
    __tablename__ = "source_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # 'gmail', 'outlook', 'upload', 'api', etc.
    name = Column(String(255), nullable=False)
    credentials = Column(JSONB)  # Encrypted OAuth tokens, API keys
    settings = Column(JSONB)  # Provider-specific settings
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    items = relationship("InReviewItem", back_populates="source")


class DestinationConfig(Base):
    __tablename__ = "destination_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # 'github', 'gdrive', 'email', etc.
    name = Column(String(255), nullable=False)
    credentials = Column(JSONB)  # Encrypted credentials
    settings = Column(JSONB)  # Destination-specific settings (repo, folder, etc.)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InReviewItem(Base):
    __tablename__ = "in_review_item"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(Integer, ForeignKey("source_config.id"))
    category = Column(Enum(CategoryType))
    content = Column(Text)  # Raw content or file path
    metadata = Column(JSONB)  # File size, type, original headers, etc.
    preview_url = Column(String(1024))
    search_vector = Column(TSVECTOR)  # Full-text search
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="items")
    source = relationship("SourceConfig", back_populates="items")
    attachments = relationship("Attachment", back_populates="item", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="item_tag", back_populates="items")
    routing_jobs = relationship("RoutingJob", back_populates="item")
    
    __table_args__ = (
        Index('idx_item_created_at_desc', created_at.desc()),
        Index('idx_item_search_vector', search_vector, postgresql_using='gin'),
    )


class Attachment(Base):
    __tablename__ = "attachment"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("in_review_item.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)  # S3/local path
    category = Column(Enum(CategoryType))
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("InReviewItem", back_populates="attachments")


class Tag(Base):
    __tablename__ = "tag"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    items = relationship("InReviewItem", secondary="item_tag", back_populates="tags")


class ItemTag(Base):
    __tablename__ = "item_tag"
    
    item_id = Column(Integer, ForeignKey("in_review_item.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)


class RoutingRule(Base):
    __tablename__ = "routing_rule"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    conditions = Column(JSONB, nullable=False)  # e.g., {"category": "code", "source_type": "gmail"}
    destination_ids = Column(JSONB, nullable=False)  # Array of destination IDs
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="routing_rules")


class AutoSortRule(Base):
    __tablename__ = "auto_sort_rule"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    conditions = Column(JSONB, nullable=False)  # e.g., {"from": "*@example.com", "has_attachment": true}
    actions = Column(JSONB, nullable=False)  # e.g., {"set_category": "legal", "add_tags": ["invoice"]}
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher priority rules execute first
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="auto_sort_rules")


class RoutingJob(Base):
    __tablename__ = "routing_job"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("in_review_item.id", ondelete="CASCADE"), nullable=False)
    destination_ids = Column(JSONB, nullable=False)  # Array of destination IDs
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    results = Column(JSONB)  # Results from each destination
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    item = relationship("InReviewItem", back_populates="routing_jobs")


class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    action = Column(String(100), nullable=False, index=True)  # 'ITEM_INGEST', 'ITEM_ROUTE', etc.
    entity_type = Column(String(50))  # 'item', 'rule', 'destination'
    entity_id = Column(Integer)
    details = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(String(512))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class WebhookEventLog(Base):
    __tablename__ = "webhook_event_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)  # 'email_received', 'attachment_extracted'
    source_type = Column(String(50))  # 'gmail', 'outlook', etc.
    event_data = Column(JSONB)
    user_id = Column(Integer, ForeignKey("user.id"))
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class CarbonTracking(Base):
    __tablename__ = "carbon_tracking"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(100), nullable=False)  # 'email_route', 'file_compress', etc.
    savings_grams = Column(Float, default=0.0)  # CO2 savings in grams
    details = Column(JSONB)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class ProcessingModeConfig(Base):
    __tablename__ = "processing_mode_config"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    mode = Column(Enum(ProcessingMode), nullable=False)
    is_active = Column(Boolean, default=False)
    settings = Column(JSONB)  # Mode-specific settings (e.g., date ranges for date_range mode)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
