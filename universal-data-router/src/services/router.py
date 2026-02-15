"""
Routing service - Core logic for multi-destination routing
"""

from sqlalchemy.orm import Session
from typing import List, Dict
import asyncio

from ..models.database import RoutingJob, InReviewItem, DestinationConfig, JobStatus
from ..utils.logger import setup_logger
from ..integrations.github_plugin import GitHubPlugin
from ..integrations.gdrive_plugin import GoogleDrivePlugin

logger = setup_logger(__name__)

async def route_to_destinations(job_id: int, db: Session):
    """
    Route an item to multiple destinations
    """
    job = db.query(RoutingJob).filter(RoutingJob.id == job_id).first()
    if not job:
        logger.error(f"Job {job_id} not found")
        return
    
    # Update status to running
    job.status = JobStatus.RUNNING
    db.commit()
    
    try:
        # Get item
        item = db.query(InReviewItem).filter(InReviewItem.id == job.item_id).first()
        if not item:
            raise Exception(f"Item {job.item_id} not found")
        
        # Get destinations
        destinations = db.query(DestinationConfig).filter(
            DestinationConfig.id.in_(job.destination_ids)
        ).all()
        
        # Route to each destination
        results = {}
        for dest in destinations:
            try:
                result = await route_to_single_destination(item, dest)
                results[dest.id] = {"status": "success", "result": result}
                logger.info(f"Routed item {item.id} to {dest.name}")
            except Exception as e:
                results[dest.id] = {"status": "failed", "error": str(e)}
                logger.error(f"Failed to route item {item.id} to {dest.name}: {e}")
        
        # Update job with results
        job.status = JobStatus.SUCCESS
        job.results = results
        
    except Exception as e:
        logger.error(f"Routing job {job_id} failed: {e}")
        job.status = JobStatus.FAILED
        job.error_message = str(e)
    
    finally:
        from datetime import datetime
        job.completed_at = datetime.utcnow()
        db.commit()

async def route_to_single_destination(item: InReviewItem, destination: DestinationConfig) -> Dict:
    """
    Route an item to a single destination
    """
    plugin = get_plugin_for_destination(destination)
    
    # Prepare data packet
    data_packet = {
        "id": item.id,
        "content": item.content,
        "metadata": item.metadata,
        "category": item.category.value if item.category else None
    }
    
    # Send to destination
    result = await plugin.send(data_packet)
    return result

def get_plugin_for_destination(destination: DestinationConfig):
    """
    Get the appropriate plugin for a destination
    """
    if destination.type == "github":
        return GitHubPlugin(destination.credentials, destination.settings)
    elif destination.type == "gdrive":
        return GoogleDrivePlugin(destination.credentials, destination.settings)
    else:
        raise Exception(f"Unsupported destination type: {destination.type}")
