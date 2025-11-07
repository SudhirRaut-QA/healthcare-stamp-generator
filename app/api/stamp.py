"""
Stamp generation API endpoints
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io
import logging
from app.models.schemas import StampGenerationRequest, ErrorResponse
from app.modules.stamp_generator import HospitalStampGenerator, StampStyle, StampColor

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
        
        # Generate stamp using the enhanced method with character spacing
        stamp_bytes = stamp_generator.generate_stamp(
            hospital_name=request.hospital_name,
            size=request.size,
            font_size=request.font_size,
            character_spacing=request.character_spacing
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


@router.post(
    "/generate/enhanced",
    responses={
        200: {"content": {"image/png": {}}},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate Enhanced Hospital Stamp",
    description="Generate an enhanced hospital stamp with advanced features like date, custom styles, and colors"
)
async def generate_enhanced_stamp(
    hospital_name: str,
    style: str = "classic",
    color: str = "blue", 
    size: int = 350,
    include_date: bool = False,
    include_logo: bool = True,
    border_style: str = "double"
):
    """
    Generate an enhanced hospital stamp with advanced customization options.
    
    Args:
        hospital_name: Name of the hospital
        style: Stamp style (classic, modern, official, emergency)
        color: Stamp color (blue, red, green, black, navy, maroon)
        size: Stamp size in pixels
        include_date: Include current date in stamp
        include_logo: Include medical symbol
        border_style: Border style (single, double, triple)
    """
    try:
        if not hospital_name or len(hospital_name) > 50:
            raise HTTPException(
                status_code=400, 
                detail="Hospital name must be between 1 and 50 characters"
            )
        
        # Map string parameters to enums
        style_map = {
            "classic": StampStyle.CLASSIC,
            "modern": StampStyle.MODERN,
            "official": StampStyle.OFFICIAL,
            "emergency": StampStyle.EMERGENCY
        }
        
        color_map = {
            "blue": StampColor.BLUE,
            "red": StampColor.RED,
            "green": StampColor.GREEN,
            "black": StampColor.BLACK,
            "navy": StampColor.NAVY,
            "maroon": StampColor.MAROON
        }
        
        stamp_style = style_map.get(style.lower(), StampStyle.CLASSIC)
        stamp_color = color_map.get(color.lower(), StampColor.BLUE)
        
        logger.info(f"Generating enhanced stamp for: {hospital_name} with style: {style}")
        
        # Generate enhanced stamp with character spacing
        stamp_bytes = stamp_generator.generate_stamp(
            hospital_name=hospital_name,
            size=size,
            style=stamp_style,
            color=stamp_color.value,
            include_date=include_date,
            include_logo=include_logo,
            border_style=border_style,
            character_spacing=1.2  # Optimized character spacing to prevent overlap
        )
        
        # Create filename
        safe_name = "".join(c for c in hospital_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}_{style}_stamp.png"
        
        # Return image as streaming response
        return StreamingResponse(
            io.BytesIO(stamp_bytes),
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating enhanced stamp: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating enhanced stamp")


@router.get(
    "/variants/{hospital_name}",
    responses={
        200: {"content": {"application/json": {}}},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate All Stamp Variants",
    description="Generate all available stamp variants (classic, modern, official, emergency) for a hospital"
)
async def generate_stamp_variants(hospital_name: str):
    """
    Generate all available stamp variants for a hospital.
    Returns JSON with download links for each variant.
    """
    try:
        if not hospital_name or len(hospital_name) > 50:
            raise HTTPException(
                status_code=400, 
                detail="Hospital name must be between 1 and 50 characters"
            )
        
        logger.info(f"Generating all variants for: {hospital_name}")
        
        # This would normally save files and return URLs
        # For this example, we'll return a JSON response with variant info
        variants = {
            "hospital_name": hospital_name,
            "variants": [
                {
                    "style": "classic",
                    "description": "Traditional blue circular stamp",
                    "download_url": f"/api/v1/stamp/generate/enhanced?hospital_name={hospital_name}&style=classic"
                },
                {
                    "style": "modern", 
                    "description": "Modern green stamp with clean design",
                    "download_url": f"/api/v1/stamp/generate/enhanced?hospital_name={hospital_name}&style=modern&color=green"
                },
                {
                    "style": "official",
                    "description": "Official navy stamp with date",
                    "download_url": f"/api/v1/stamp/generate/enhanced?hospital_name={hospital_name}&style=official&color=navy&include_date=true"
                },
                {
                    "style": "emergency",
                    "description": "Emergency red stamp for urgent use",
                    "download_url": f"/api/v1/stamp/generate/enhanced?hospital_name={hospital_name}&style=emergency&color=red"
                }
            ],
            "total_variants": 4
        }
        
        return variants
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating variants info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while generating variants info")