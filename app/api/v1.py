"""
API v1 router configuration
"""

from fastapi import APIRouter
from app.models.schemas import HealthResponse
from .stamp import router as stamp_router

# Create main v1 router
router = APIRouter()

# Include sub-routers
router.include_router(stamp_router)

@router.get(
    "/health", 
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API service is running and healthy"
)
async def health_check():
    """Health check endpoint for the API"""
    return HealthResponse(status="healthy", service="healthcare-stamp-api")