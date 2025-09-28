"""
Healthcare Application Main Module
FastAPI application for healthcare operations with stamp generation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as v1_router
from app.api.doctor_stamp_routes import router as doctor_stamp_router

# Create FastAPI application
app = FastAPI(
    title="Healthcare Operations API",
    description="A superfast and scalable healthcare application with hospital & doctor stamp generators",
    version="1.0.0",
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

# Include API routers
app.include_router(v1_router, prefix="/api/v1")
app.include_router(doctor_stamp_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Healthcare Operations API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "healthcare-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)