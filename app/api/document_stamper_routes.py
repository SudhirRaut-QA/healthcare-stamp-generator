"""
Document Stamping API Routes
FastAPI endpoints for interactive document stamping with preview functionality.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import os
import sys
import uuid
import tempfile
import shutil
from io import BytesIO
import json

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.document_stamper.document_processor import DocumentProcessor
from modules.document_stamper.stamp_overlay import StampOverlay, StampPosition
from modules.document_stamper.preview_generator import PreviewGenerator
from modules.stamp_generator.generator import HospitalStampGenerator
from modules.doctor_stamp.generator import DoctorStampGenerator

router = APIRouter(prefix="/api/v1/document-stamper", tags=["Document Stamping"])

# Global instances (in production, use proper session management)
active_sessions = {}

class DocumentSession:
    """Document stamping session."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.document_processor = DocumentProcessor()
        self.stamp_overlay = StampOverlay()
        self.preview_generator = PreviewGenerator(self.stamp_overlay)
        self.document_loaded = False
        self.document_data = None

# Pydantic Models
class SessionResponse(BaseModel):
    session_id: str
    success: bool
    message: str

class DocumentUploadResponse(BaseModel):
    success: bool
    session_id: str
    document_type: str
    page_count: int
    metadata: dict
    pages: List[dict]

class StampAddRequest(BaseModel):
    session_id: str
    page_number: int
    stamp_type: str = Field(..., pattern="^(hospital|doctor)$")
    x: float = Field(0.5, ge=0.0, le=1.0)
    y: float = Field(0.5, ge=0.0, le=1.0)
    width: Optional[int] = Field(None, ge=50, le=800)
    height: Optional[int] = Field(None, ge=50, le=800)
    
    # Hospital stamp data
    hospital_name: Optional[str] = None
    
    # Doctor stamp data
    doctor_name: Optional[str] = None
    degree: Optional[str] = None
    registration_number: Optional[str] = None

class StampMoveRequest(BaseModel):
    session_id: str
    stamp_id: str
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)

class StampResizeRequest(BaseModel):
    session_id: str
    stamp_id: str
    width: int = Field(..., ge=50, le=800)
    height: int = Field(..., ge=50, le=800)

class StampRotateRequest(BaseModel):
    session_id: str
    stamp_id: str
    rotation: float = Field(..., ge=0.0, lt=360.0)

class StampOpacityRequest(BaseModel):
    session_id: str
    stamp_id: str
    opacity: float = Field(..., ge=0.0, le=1.0)

class StampDeleteRequest(BaseModel):
    session_id: str
    stamp_id: str

class PreviewRequest(BaseModel):
    session_id: str
    page_number: int
    preview_width: Optional[int] = Field(None, ge=200, le=2000)
    preview_height: Optional[int] = Field(None, ge=200, le=2000)
    show_boundaries: bool = False

# Helper Functions
def get_session(session_id: str) -> DocumentSession:
    """Get document session by ID."""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return active_sessions[session_id]

def validate_page_number(session: DocumentSession, page_number: int):
    """Validate page number exists."""
    if not session.document_loaded:
        raise HTTPException(status_code=400, detail="No document loaded in session")
    
    if page_number < 1 or page_number > session.document_processor.get_page_count():
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid page number. Document has {session.document_processor.get_page_count()} pages"
        )

# API Endpoints
@router.post("/session/create", response_model=SessionResponse)
async def create_session():
    """Create a new document stamping session."""
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = DocumentSession(session_id)
    
    return SessionResponse(
        session_id=session_id,
        success=True,
        message="Document stamping session created successfully"
    )

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a document stamping session."""
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"success": True, "message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.post("/document/upload", response_model=DocumentUploadResponse)
async def upload_document(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload a document (PDF or image) for stamping."""
    session = get_session(session_id)
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Read file data
    try:
        file_data = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
    
    # Process document
    try:
        document_result = session.document_processor.load_document_from_bytes(
            file_data, file.filename
        )
        
        session.document_loaded = True
        session.document_data = document_result
        
        return DocumentUploadResponse(
            success=True,
            session_id=session_id,
            document_type=document_result['document_type'],
            page_count=document_result['page_count'],
            metadata=document_result['metadata'],
            pages=document_result['pages']
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process document: {str(e)}")

@router.get("/document/{session_id}/info")
async def get_document_info(session_id: str):
    """Get document information."""
    session = get_session(session_id)
    
    if not session.document_loaded:
        raise HTTPException(status_code=400, detail="No document loaded in session")
    
    return {
        "success": True,
        "document_data": session.document_data,
        "stamps_summary": session.stamp_overlay.get_stamps_summary()
    }

@router.post("/stamp/add")
async def add_stamp(request: StampAddRequest):
    """Add a stamp to a document page."""
    session = get_session(request.session_id)
    validate_page_number(session, request.page_number)
    
    try:
        # Generate stamp based on type
        if request.stamp_type == 'hospital':
            if not request.hospital_name:
                raise HTTPException(status_code=400, detail="Hospital name required for hospital stamp")
            
            generator = HospitalStampGenerator()
            stamp_bytes = generator.generate_stamp(request.hospital_name)
            
            # Convert bytes to PIL Image
            from PIL import Image
            from io import BytesIO
            stamp_image = Image.open(BytesIO(stamp_bytes))
            
            stamp_data = {"hospital_name": request.hospital_name, "type": "hospital"}
            
        elif request.stamp_type == 'doctor':
            if not all([request.doctor_name, request.degree, request.registration_number]):
                raise HTTPException(
                    status_code=400, 
                    detail="Doctor name, degree, and registration number required for doctor stamp"
                )
            
            generator = DoctorStampGenerator()
            stamp_file_path = generator.generate_doctor_stamp(
                request.doctor_name,
                request.degree,
                request.registration_number
            )
            
            # Load the generated stamp image
            from PIL import Image
            stamp_image = Image.open(stamp_file_path)
            
            stamp_data = {
                "doctor_name": request.doctor_name,
                "degree": request.degree,
                "registration_number": request.registration_number,
                "type": "doctor"
            }
        
        # Add stamp to overlay
        stamp_id = session.stamp_overlay.add_stamp(
            page_number=request.page_number,
            stamp_type=request.stamp_type,
            stamp_image=stamp_image,
            stamp_data=stamp_data,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height
        )
        
        return {
            "success": True,
            "stamp_id": stamp_id,
            "message": f"{request.stamp_type.title()} stamp added successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add stamp: {str(e)}")

@router.put("/stamp/move")
async def move_stamp(request: StampMoveRequest):
    """Move a stamp to a new position."""
    session = get_session(request.session_id)
    
    success = session.stamp_overlay.move_stamp(request.stamp_id, request.x, request.y)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    return {"success": True, "message": "Stamp moved successfully"}

@router.put("/stamp/resize")
async def resize_stamp(request: StampResizeRequest):
    """Resize a stamp."""
    session = get_session(request.session_id)
    
    success = session.stamp_overlay.resize_stamp(request.stamp_id, request.width, request.height)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    return {"success": True, "message": "Stamp resized successfully"}

@router.put("/stamp/rotate")
async def rotate_stamp(request: StampRotateRequest):
    """Rotate a stamp."""
    session = get_session(request.session_id)
    
    success = session.stamp_overlay.rotate_stamp(request.stamp_id, request.rotation)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    return {"success": True, "message": "Stamp rotated successfully"}

@router.put("/stamp/opacity")
async def set_stamp_opacity(request: StampOpacityRequest):
    """Set stamp opacity."""
    session = get_session(request.session_id)
    
    success = session.stamp_overlay.set_stamp_opacity(request.stamp_id, request.opacity)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    return {"success": True, "message": "Stamp opacity updated successfully"}

@router.delete("/stamp/delete")
async def delete_stamp(request: StampDeleteRequest):
    """Delete a stamp."""
    session = get_session(request.session_id)
    
    success = session.stamp_overlay.remove_stamp(request.stamp_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    return {"success": True, "message": "Stamp deleted successfully"}

@router.post("/preview/page")
async def generate_page_preview(request: PreviewRequest):
    """Generate preview of a page with stamps."""
    session = get_session(request.session_id)
    validate_page_number(session, request.page_number)
    
    # Get page data
    page_data = session.document_processor.get_page(request.page_number)
    if not page_data:
        raise HTTPException(status_code=404, detail="Page not found")
    
    try:
        preview_result = session.preview_generator.generate_page_preview(
            page_data['image'],
            request.page_number,
            request.preview_width,
            request.preview_height,
            request.show_boundaries
        )
        
        # Remove PIL image from response (not JSON serializable)
        preview_result.pop('preview_image', None)
        
        return preview_result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate preview: {str(e)}")

@router.get("/preview/page/{session_id}/{page_number}/image")
async def get_page_preview_image(
    session_id: str,
    page_number: int,
    preview_width: Optional[int] = None,
    preview_height: Optional[int] = None,
    show_boundaries: bool = False
):
    """Get page preview as PNG image."""
    session = get_session(session_id)
    validate_page_number(session, page_number)
    
    page_data = session.document_processor.get_page(page_number)
    if not page_data:
        raise HTTPException(status_code=404, detail="Page not found")
    
    try:
        preview_result = session.preview_generator.generate_page_preview(
            page_data['image'],
            page_number,
            preview_width,
            preview_height,
            show_boundaries
        )
        
        # Return image as PNG
        img_buffer = BytesIO()
        preview_result['preview_image'].save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return StreamingResponse(
            io=img_buffer,
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=page_{page_number}_preview.png"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate preview image: {str(e)}")

@router.get("/stamps/{session_id}/list")
async def list_stamps(session_id: str, page_number: Optional[int] = None):
    """List stamps in session or on specific page."""
    session = get_session(session_id)
    
    if page_number:
        validate_page_number(session, page_number)
        stamps = session.stamp_overlay.get_page_stamps(page_number)
        return {
            "success": True,
            "page_number": page_number,
            "stamps": [stamp.to_dict() for stamp in stamps]
        }
    else:
        summary = session.stamp_overlay.get_stamps_summary()
        return {
            "success": True,
            "summary": summary
        }

@router.get("/stamps/{session_id}/export")
async def export_stamp_configuration(session_id: str):
    """Export stamp configuration as JSON."""
    session = get_session(session_id)
    
    config_json = session.stamp_overlay.export_stamps_config()
    
    return Response(
        content=config_json,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=stamps_config_{session_id[:8]}.json"
        }
    )

@router.post("/stamps/{session_id}/import")
async def import_stamp_configuration(
    session_id: str,
    file: UploadFile = File(...)
):
    """Import stamp configuration from JSON."""
    session = get_session(session_id)
    
    if not file.filename or not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Please upload a JSON file")
    
    try:
        config_data = await file.read()
        config_json = config_data.decode('utf-8')
        
        success = session.stamp_overlay.import_stamps_config(config_json)
        
        if not success:
            raise HTTPException(status_code=400, detail="Invalid configuration file format")
        
        return {
            "success": True,
            "message": "Stamp configuration imported successfully",
            "summary": session.stamp_overlay.get_stamps_summary()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to import configuration: {str(e)}")

@router.delete("/stamps/{session_id}/clear")
async def clear_stamps(session_id: str, page_number: Optional[int] = None):
    """Clear stamps from session or specific page."""
    session = get_session(session_id)
    
    if page_number:
        validate_page_number(session, page_number)
        count = session.stamp_overlay.clear_page_stamps(page_number)
        return {
            "success": True,
            "message": f"Cleared {count} stamps from page {page_number}"
        }
    else:
        count = session.stamp_overlay.clear_all_stamps()
        return {
            "success": True,
            "message": f"Cleared {count} stamps from all pages"
        }

@router.get("/sessions/list")
async def list_active_sessions():
    """List all active stamping sessions."""
    sessions_info = []
    
    for session_id, session in active_sessions.items():
        info = {
            "session_id": session_id,
            "document_loaded": session.document_loaded,
            "stamps_summary": session.stamp_overlay.get_stamps_summary()
        }
        
        if session.document_loaded:
            info["document_metadata"] = session.document_processor.get_metadata()
        
        sessions_info.append(info)
    
    return {
        "success": True,
        "active_sessions": len(active_sessions),
        "sessions": sessions_info
    }

@router.get("/health")
async def health_check():
    """Health check endpoint for document stamping service."""
    return {
        "status": "healthy",
        "service": "Document Stamping API",
        "active_sessions": len(active_sessions),
        "features": [
            "PDF and image document processing",
            "Interactive stamp placement",
            "Real-time preview generation",
            "Stamp manipulation (move, resize, rotate, opacity)",
            "Multi-page document support",
            "Configuration import/export"
        ]
    }