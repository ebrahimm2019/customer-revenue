"""
Customer Revenue Intelligence Platform
Main FastAPI Application - Dynamic with Real Data
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os, pickle, json
import pandas as pd
import numpy as np
from pathlib import Path

from app.api.customers import router as customers_router
from app.api.predictions import router as predictions_router
from app.api.campaigns import router as campaigns_router
from app.api.analytics import router as analytics_router

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Global state
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading data and models...")

    # Load customer features
    cf = pd.read_csv(DATA_DIR / "customer_features.csv", index_col=0)
    app_state['customers'] = cf

    # Load model
    model_path = MODELS_DIR / "three_stage_model.pkl"
    if model_path.exists():
        with open(model_path, 'rb') as f:
            app_state['model'] = pickle.load(f)
        print(f"✓ Three-Stage model loaded")

    # Load supporting data
    for fname in ['model_results.json', 'segment_summary.json', 'cleaning_summary.json', 'revenue_capture.json']:
        fpath = DATA_DIR / fname
        if fpath.exists():
            with open(fpath) as f:
                app_state[fname.replace('.json', '')] = json.load(f)

    for fname in ['monthly_revenue.csv', 'feature_importance.csv', 'feature_correlations.csv',
                   'top_products.csv', 'country_data.csv']:
        fpath = DATA_DIR / fname
        if fpath.exists():
            app_state[fname.replace('.csv', '')] = pd.read_csv(fpath)

    print(f"✓ Loaded {len(app_state['customers']):,} customers")
    print(f"✓ Loaded {len(app_state.get('model_results', {}))} model results")
    yield
    print("Shutting down...")

app = FastAPI(
    title="Customer Revenue Intelligence",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers_router, prefix="/api", tags=["Customers"])
app.include_router(predictions_router, prefix="/api", tags=["Predictions"])
app.include_router(campaigns_router, prefix="/api", tags=["Campaigns"])
app.include_router(analytics_router, prefix="/api", tags=["Analytics"])

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "customers_loaded": len(app_state.get('customers', [])),
        "model_loaded": 'model' in app_state,
    }

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)), reload=True)
