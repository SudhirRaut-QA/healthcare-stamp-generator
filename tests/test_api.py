"""
Tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_api_health_check(self):
        """Test API v1 health check"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "healthcare-stamp-api"
    
    def test_generate_stamp_success(self):
        """Test successful stamp generation"""
        payload = {
            "hospital_name": "City General Hospital",
            "size": 300
        }
        response = client.post("/api/v1/stamp/generate", json=payload)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0
    
    def test_generate_stamp_invalid_name(self):
        """Test stamp generation with invalid hospital name"""
        payload = {
            "hospital_name": "",  # Empty name
            "size": 300
        }
        response = client.post("/api/v1/stamp/generate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_generate_stamp_invalid_size(self):
        """Test stamp generation with invalid size"""
        payload = {
            "hospital_name": "Test Hospital",
            "size": 50  # Too small
        }
        response = client.post("/api/v1/stamp/generate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_preview_stamp_success(self):
        """Test successful stamp preview"""
        hospital_name = "Test Hospital"
        response = client.get(f"/api/v1/stamp/preview/{hospital_name}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0
    
    def test_preview_stamp_with_size(self):
        """Test stamp preview with custom size"""
        hospital_name = "Test Hospital"
        response = client.get(f"/api/v1/stamp/preview/{hospital_name}?size=400")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0
    
    def test_preview_stamp_empty_name(self):
        """Test stamp preview with empty name"""
        response = client.get("/api/v1/stamp/preview/")
        assert response.status_code == 404  # Not found due to empty path
    
    def test_api_documentation(self):
        """Test that API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]