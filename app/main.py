"""
Customer Revenue Intelligence Platform - Production Ready
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
import os
from pathlib import Path

# Import routers
from app.api.customers import router as customers_router
from app.api.predictions import router as predictions_router
from app.api.campaigns import router as campaigns_router
from app.api.analytics import router as analytics_router

# Configuration
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"

# Ensure directories exist
STATIC_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# Lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Customer Revenue Intelligence Platform...")
    print(f"📁 Static directory: {STATIC_DIR}")
    print(f"📤 Uploads directory: {UPLOADS_DIR}")
    
    # Load ML model if exists
    model_path = BASE_DIR / "models" / "trained_model.pkl"
    if model_path.exists():
        print(f"✓ Model found: {model_path}")
        # TODO: Load model into memory
    else:
        print(f"⚠ No model found at {model_path}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Customer Revenue Intelligence",
    description="Predictive analytics and customer segmentation platform",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(customers_router, prefix="/api", tags=["Customers"])
app.include_router(predictions_router, prefix="/api", tags=["Predictions"])
app.include_router(campaigns_router, prefix="/api", tags=["Campaigns"])
app.include_router(analytics_router, prefix="/api", tags=["Analytics"])

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    # Fallback HTML if no index.html
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Revenue Intelligence</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #0F1419;
                color: #E8EAED;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                max-width: 600px;
                padding: 40px;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 16px;
            }
            p {
                font-size: 18px;
                color: #9AA0A6;
                margin-bottom: 32px;
            }
            .links {
                display: flex;
                gap: 16px;
                justify-content: center;
            }
            a {
                padding: 12px 24px;
                background: #8AB4F8;
                color: #0F1419;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.2s;
            }
            a:hover {
                background: #A8C7FA;
                transform: translateY(-2px);
            }
            .status {
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #4CAF50;
                border-radius: 50%;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Customer Revenue Intelligence</h1>
            <p><span class="status"></span> System is running</p>
            <div class="links">
                <a href="/docs">API Documentation</a>
                <a href="/api/health">Health Check</a>
            </div>
        </div>
    </body>
    </html>
    """

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check for Railway"""
    return {
        "status": "healthy",
        "service": "Customer Revenue Intelligence",
        "version": "2.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

# Serve static files (CSS, JS, images)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Run with: uvicorn app.main:app --host 0.0.0.0 --port 8000
