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
    character_spacing: Optional[float] = Field(
        1.2,
        description="Character spacing multiplier for optimal readability (1.0=normal, 1.2=improved spacing without overlap)",
        ge=0.8,
        le=2.5
    )


class EnhancedStampRequest(BaseModel):
    """Request model for enhanced stamp generation"""
    hospital_name: str = Field(
        ..., 
        description="Name of the hospital for the stamp",
        min_length=1,
        max_length=50
    )
    size: Optional[int] = Field(
        350, 
        description="Size of the stamp in pixels (diameter)",
        ge=100,
        le=800
    )
    style: Optional[str] = Field(
        "classic",
        description="Stamp style: classic, modern, official, emergency"
    )
    color: Optional[str] = Field(
        "blue",
        description="Stamp color: blue, red, green, black, navy, maroon"
    )
    include_date: Optional[bool] = Field(
        False,
        description="Include current date in the stamp"
    )
    include_logo: Optional[bool] = Field(
        True,
        description="Include medical symbol in the stamp"
    )
    border_style: Optional[str] = Field(
        "double",
        description="Border style: single, double, triple"
    )
    character_spacing: Optional[float] = Field(
        1.2,
        description="Character spacing multiplier for optimal readability (1.0=normal, 1.2=improved spacing without overlap)",
        ge=0.8,
        le=2.5
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