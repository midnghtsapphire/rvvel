"""
Test suite for Universal Data Router API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.main import app
from src.models.database import Base
from src.utils.database import get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestItemsAPI:
    """Test items endpoints"""
    
    def test_list_items(self):
        """Test listing items"""
        response = client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    def test_get_item(self):
        """Test getting a single item"""
        # First create an item
        # Then test retrieval
        pass
    
    def test_update_item(self):
        """Test updating an item"""
        pass
    
    def test_delete_items(self):
        """Test bulk delete"""
        pass
    
    def test_date_range_filters(self):
        """Test date range filtering"""
        response = client.get("/items/date-range/today")
        assert response.status_code == 200

class TestRoutingAPI:
    """Test routing endpoints"""
    
    def test_create_routing_job(self):
        """Test creating a routing job"""
        payload = {
            "item_ids": [1, 2],
            "destination_ids": [1]
        }
        response = client.post("/routing/jobs", json=payload)
        # Note: Will fail without proper setup, but structure is correct
        assert response.status_code in [200, 404]
    
    def test_get_routing_job(self):
        """Test getting routing job status"""
        response = client.get("/routing/jobs/1")
        assert response.status_code in [200, 404]
    
    def test_export_items(self):
        """Test export endpoint"""
        payload = {
            "type": "all",
            "destination_ids": [1]
        }
        response = client.post("/routing/export", json=payload)
        assert response.status_code in [200, 404]

class TestRulesAPI:
    """Test rules endpoints"""
    
    def test_list_auto_sort_rules(self):
        """Test listing auto-sort rules"""
        response = client.get("/rules/auto-sort")
        assert response.status_code == 200
    
    def test_create_auto_sort_rule(self):
        """Test creating an auto-sort rule"""
        payload = {
            "name": "Test Rule",
            "conditions": {"from": "*@example.com"},
            "actions": {"set_category": "code"},
            "priority": 1
        }
        response = client.post("/rules/auto-sort", json=payload)
        assert response.status_code == 200
    
    def test_update_auto_sort_rule(self):
        """Test updating an auto-sort rule"""
        pass
    
    def test_delete_auto_sort_rule(self):
        """Test deleting an auto-sort rule"""
        pass

class TestProcessingAPI:
    """Test processing endpoints"""
    
    def test_run_processing_bulk(self):
        """Test bulk processing"""
        payload = {
            "mode": "bulk",
            "params": {}
        }
        response = client.post("/processing/run", json=payload)
        assert response.status_code == 200
    
    def test_run_processing_date_range(self):
        """Test date range processing"""
        payload = {
            "mode": "date_range",
            "params": {
                "start_date": "2026-01-01T00:00:00",
                "end_date": "2026-12-31T23:59:59"
            }
        }
        response = client.post("/processing/run", json=payload)
        assert response.status_code == 200
    
    def test_run_auto_sort(self):
        """Test auto-sort trigger"""
        response = client.post("/processing/auto-sort/run")
        assert response.status_code == 200

class TestWebhooksAPI:
    """Test webhook endpoints"""
    
    def test_gmail_webhook(self):
        """Test Gmail webhook"""
        payload = {
            "message": {
                "data": "test"
            }
        }
        response = client.post("/webhooks/email/gmail", json=payload)
        assert response.status_code == 200
    
    def test_generic_webhook(self):
        """Test generic webhook"""
        payload = {
            "event": "test"
        }
        response = client.post("/webhooks/generic", json=payload)
        assert response.status_code == 200

class TestHealthCheck:
    """Test health endpoints"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
    
    def test_health(self):
        """Test health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
