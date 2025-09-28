"""
Stamp generation API endpoints
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io
import logging
from app.models.schemas import StampGenerationRequest, ErrorResponse
from app.modules.stamp_generator import HospitalStampGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stamp", tags=["Stamp Generation"])

# Initialize stamp generator
stamp_generator = HospitalStampGenerator()


@router.post(
    "/generate",
    responses={
        200: {"content": {"image/png": {}}},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate Hospital Stamp",
    description="Generate a circular hospital stamp with transparent background in PNG format"
)
async def generate_stamp(request: StampGenerationRequest):
    """
    Generate a hospital stamp based on the provided hospital name.
    
    Returns a PNG image with:
    - Circular design with blue ink color
    - Transparent background for prescription printing
    - Professional medical stamp appearance
    """
    try:
        logger.info(f"Generating stamp for hospital: {request.hospital_name}")
        
        # Generate stamp
        stamp_bytes = stamp_generator.generate_stamp(
            hospital_name=request.hospital_name,
            size=request.size,
            font_size=request.font_size
        )
        
        # Create filename
        safe_name = "".join(c for c in request.hospital_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}_hospital_stamp.png"
        
        # Return image as streaming response
        return StreamingResponse(
            io.BytesIO(stamp_bytes),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating stamp: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating stamp")


@router.get(
    "/preview/{hospital_name}",
    responses={
        200: {"content": {"image/png": {}}},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Preview Hospital Stamp",
    description="Generate a preview of hospital stamp with default settings"
)
async def preview_stamp(hospital_name: str, size: int = 300):
    """
    Generate a preview of a hospital stamp with default settings.
    
    Args:
        hospital_name: Name of the hospital
        size: Optional size parameter (default: 300px)
    """
    try:
        if not hospital_name or len(hospital_name) > 50:
            raise HTTPException(
                status_code=400, 
                detail="Hospital name must be between 1 and 50 characters"
            )
        
        logger.info(f"Generating preview stamp for: {hospital_name}")
        
        # Generate stamp with default settings
        stamp_bytes = stamp_generator.generate_stamp(
            hospital_name=hospital_name,
            size=size
        )
        
        # Return image directly
        return StreamingResponse(
            io.BytesIO(stamp_bytes),
            media_type="image/png"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating preview")