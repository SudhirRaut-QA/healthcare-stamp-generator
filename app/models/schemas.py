"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, Tuple


class StampGenerationRequest(BaseModel):
    """Request model for stamp generation"""
    hospital_name: str = Field(
        ..., 
        description="Name of the hospital for the stamp",
        min_length=1,
        max_length=50
    )
    size: Optional[int] = Field(
        300, 
        description="Size of the stamp in pixels (diameter)",
        ge=100,
        le=800
    )
    font_size: Optional[int] = Field(
        None,
        description="Font size for text (auto-calculated if not provided)",
        ge=8,
        le=50
    )


class StampGenerationResponse(BaseModel):
    """Response model for stamp generation"""
    message: str = Field(description="Success message")
    filename: str = Field(description="Generated filename")
    size: int = Field(description="Stamp size in pixels")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Error details")