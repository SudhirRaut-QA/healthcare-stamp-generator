"""
Doctor Stamp API Routes

FastAPI endpoints for generating professional doctor stamps.
"""

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field, validator
import os
import sys
from typing import Optional

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.doctor_stamp.generator import DoctorStampGenerator

router = APIRouter(prefix="/api/v1/doctor-stamp", tags=["Doctor Stamps"])


class DoctorStampRequest(BaseModel):
    """Request model for doctor stamp generation."""
    
    doctor_name: str = Field(..., min_length=1, max_length=100, 
                           description="Doctor's full name", 
                           example="Dr. Sarah Johnson")
    degree: str = Field(..., min_length=1, max_length=200,
                       description="Medical degree and qualifications",
                       example="MBBS, MD (Cardiology)")
    registration_number: str = Field(..., min_length=1, max_length=100,
                                   description="Medical registration number (prefix 'Reg. No.:' will be auto-added)",
                                   example="MCI-12345")
    width: Optional[int] = Field(400, ge=200, le=800,
                                description="Stamp width in pixels")
    height: Optional[int] = Field(200, ge=100, le=400,
                                 description="Stamp height in pixels")
    
    @validator("doctor_name")
    def validate_doctor_name(cls, v):
        if not v.strip():
            raise ValueError("Doctor name cannot be empty")
        return v.strip()
    
    @validator("degree")
    def validate_degree(cls, v):
        if not v.strip():
            raise ValueError("Degree cannot be empty")
        return v.strip()
    
    @validator("registration_number")
    def validate_registration(cls, v):
        if not v.strip():
            raise ValueError("Registration number cannot be empty")
        return v.strip()


class DoctorStampResponse(BaseModel):
    """Response model for doctor stamp generation."""
    
    success: bool = Field(description="Whether the generation was successful")
    message: str = Field(description="Success or error message")
    file_path: Optional[str] = Field(None, description="Path to generated stamp file")
    doctor_name: Optional[str] = Field(None, description="Doctor's name from request")
    dimensions: Optional[dict] = Field(None, description="Stamp dimensions")


class BatchDoctorStampRequest(BaseModel):
    """Request model for batch doctor stamp generation."""
    
    doctors: list[DoctorStampRequest] = Field(..., min_items=1, max_items=10,
                                            description="List of doctor stamp requests")


class BatchDoctorStampResponse(BaseModel):
    """Response model for batch doctor stamp generation."""
    
    success: bool = Field(description="Whether the batch generation was successful")
    message: str = Field(description="Success or error message")
    generated_count: int = Field(description="Number of stamps successfully generated")
    failed_count: int = Field(description="Number of stamps that failed to generate")
    results: list[DoctorStampResponse] = Field(description="Individual generation results")


@router.post("/generate", response_model=DoctorStampResponse)
async def generate_doctor_stamp(request: DoctorStampRequest):
    """
    Generate a professional doctor stamp.
    
    Creates a rectangular doctor stamp with:
    - Doctor's name (largest, bold font with shadow enhancement)
    - Medical degree/qualification (medium font)
    - Registration number (smallest font)
    - Clean borderless layout
    - Vibrant bright blue text (#0066FF) for maximum visibility
    - Realistic medical fonts (Times New Roman priority)
    - Transparent PNG background
    
    Returns the generated stamp as PNG image data.
    """
    try:
        generator = DoctorStampGenerator()
        
        # Generate the stamp
        file_path = generator.generate_doctor_stamp(
            doctor_name=request.doctor_name,
            degree=request.degree,
            registration_number=request.registration_number,
            width=request.width,
            height=request.height
        )
        
        return DoctorStampResponse(
            success=True,
            message="Doctor stamp generated successfully",
            file_path=file_path,
            doctor_name=request.doctor_name,
            dimensions={"width": request.width, "height": request.height}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate doctor stamp: {str(e)}")


@router.post("/generate/image", responses={200: {"content": {"image/png": {}}}})
async def generate_doctor_stamp_image(request: DoctorStampRequest):
    """
    Generate a doctor stamp and return the PNG image directly.
    
    This endpoint returns the actual image data instead of a file path,
    making it perfect for web applications and direct integration.
    """
    try:
        generator = DoctorStampGenerator()
        
        # Generate the stamp
        file_path = generator.generate_doctor_stamp(
            doctor_name=request.doctor_name,
            degree=request.degree,
            registration_number=request.registration_number,
            width=request.width,
            height=request.height
        )
        
        # Read the generated image file
        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Clean up the temporary file
        try:
            os.remove(file_path)
        except:
            pass  # File cleanup is optional
        
        return Response(content=image_data, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate doctor stamp: {str(e)}")


@router.post("/generate/batch", response_model=BatchDoctorStampResponse)
async def generate_batch_doctor_stamps(request: BatchDoctorStampRequest):
    """
    Generate multiple doctor stamps in a single request.
    
    Useful for healthcare facilities that need to generate stamps
    for multiple doctors at once.
    """
    try:
        generator = DoctorStampGenerator()
        results = []
        generated_count = 0
        failed_count = 0
        
        for doctor_request in request.doctors:
            try:
                file_path = generator.generate_doctor_stamp(
                    doctor_name=doctor_request.doctor_name,
                    degree=doctor_request.degree,
                    registration_number=doctor_request.registration_number,
                    width=doctor_request.width,
                    height=doctor_request.height
                )
                
                results.append(DoctorStampResponse(
                    success=True,
                    message="Generated successfully",
                    file_path=file_path,
                    doctor_name=doctor_request.doctor_name,
                    dimensions={"width": doctor_request.width, "height": doctor_request.height}
                ))
                generated_count += 1
                
            except Exception as e:
                results.append(DoctorStampResponse(
                    success=False,
                    message=f"Failed to generate: {str(e)}",
                    doctor_name=doctor_request.doctor_name
                ))
                failed_count += 1
        
        return BatchDoctorStampResponse(
            success=failed_count == 0,
            message=f"Generated {generated_count} stamps, {failed_count} failed",
            generated_count=generated_count,
            failed_count=failed_count,
            results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch generation failed: {str(e)}")


@router.get("/health")
async def doctor_stamp_health_check():
    """Health check endpoint for doctor stamp service."""
    return {
        "status": "healthy",
        "service": "Doctor Stamp Generator",
        "version": "1.0.0",
        "features": [
            "Clean rectangular layout",
            "Three-tier text hierarchy",
            "Vibrant bright blue text (#0066FF)",
            "Realistic medical fonts",
            "Enhanced visibility with shadows",
            "Borderless design",
            "Transparent background",
            "Scalable sizing"
        ]
    }