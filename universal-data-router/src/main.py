"""
Universal Data Router (Revvel) - Main FastAPI Application
Production-grade backend with all features
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from typing import List, Optional
import logging
import os

from .api import items, routing, rules, sources, destinations, webhooks, processing
from .models.database import Base
from .utils.database import engine, get_db
from .utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Universal Data Router (Revvel)")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created/verified")
    
    yield
    
    logger.info("🛑 Shutting down Universal Data Router")

# Create FastAPI app
app = FastAPI(
    title="Universal Data Router (Revvel)",
    description="Route data from ANY source to ANY destination with multi-select",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(routing.router, prefix="/routing", tags=["Routing"])
app.include_router(rules.router, prefix="/rules", tags=["Rules"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(destinations.router, prefix="/destinations", tags=["Destinations"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(processing.router, prefix="/processing", tags=["Processing"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Universal Data Router (Revvel)",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # Keep connection alive and send updates
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "data": data})
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
