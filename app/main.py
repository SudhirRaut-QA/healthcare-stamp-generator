"""
Healthcare Application Main Module
FastAPI application for healthcare operations with stamp generation and document stamping
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from app.api.v1 import router as v1_router
from app.api.doctor_stamp_routes import router as doctor_stamp_router
from app.api.document_stamper_routes import router as document_stamper_router
import os

# Create FastAPI application
app = FastAPI(
    title="Healthcare Operations API",
    description="A comprehensive healthcare application with stamp generators and interactive document stamping",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API routers
app.include_router(v1_router, prefix="/api/v1")
app.include_router(doctor_stamp_router)
app.include_router(document_stamper_router)

@app.get("/")
async def root():
    """Root endpoint - redirect to document stamper"""
    return HTMLResponse("""
    <html>
        <head>
            <title>Healthcare Operations API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                .container { background: white; padding: 40px; border-radius: 15px; max-width: 800px; margin: 0 auto; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
                h1 { color: #0066ff; margin-bottom: 20px; }
                .feature { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #0066ff; }
                .btn { background: linear-gradient(135deg, #0066ff 0%, #0052cc 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; margin: 10px 5px; font-weight: 500; }
                .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏥 Healthcare Operations API v2.0.0</h1>
                <p>Welcome to the comprehensive healthcare application with stamp generators and interactive document stamping!</p>
                
                <div class="feature">
                    <h3>🔖 Interactive Document Stamper</h3>
                    <p>Upload prescriptions, invoices, or any healthcare documents and add stamps with drag & drop functionality.</p>
                    <a href="/static/document_stamper.html" class="btn">Launch Document Stamper</a>
                </div>
                
                <div class="feature">
                    <h3>🏥 Hospital Stamp Generator</h3>
                    <p>Generate professional circular hospital stamps with dynamic spacing and precision.</p>
                </div>
                
                <div class="feature">
                    <h3>🩺 Doctor Stamp Generator</h3>
                    <p>Create rectangular doctor stamps with auto-prefix registration numbers.</p>
                </div>
                
                <div class="feature">
                    <h3>🌐 API Documentation</h3>
                    <p>Complete REST API for all stamp generation and document stamping operations.</p>
                    <a href="/docs" class="btn">API Documentation</a>
                    <a href="/redoc" class="btn">ReDoc</a>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p><strong>New Features in v2.0.0:</strong></p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Interactive document stamping with preview</li>
                        <li>Drag & drop document upload (PDF, images)</li>
                        <li>Click-to-place stamp positioning</li>
                        <li>Real-time preview with stamp overlays</li>
                        <li>Multi-page document support</li>
                        <li>Stamp manipulation (move, resize, delete)</li>
                        <li>Configuration export/import</li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """)

@app.get("/stamper")
async def document_stamper():
    """Serve the document stamper interface"""
    static_path = os.path.join(static_dir, "document_stamper.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    else:
        return HTMLResponse("<h1>Document Stamper not found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "healthcare-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)