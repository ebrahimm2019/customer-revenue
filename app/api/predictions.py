"""
Predictions API Routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from enum import Enum
import pandas as pd
import io

router = APIRouter()

class SegmentEnum(str, Enum):
    VIP = "VIP"
    HIGH_VALUE = "High Value"
    GROWTH = "Growth"
    AT_RISK = "At Risk"

class PredictionRequest(BaseModel):
    customerId: int
    frequency: int
    monetary: float
    recency: int

class PredictionResponse(BaseModel):
    customerId: int
    predictedRevenue: float
    segment: SegmentEnum
    confidence: float
    recommendations: List[str]

@router.post("/predict", response_model=PredictionResponse)
async def predict_revenue(request: PredictionRequest):
    """Predict 6-month revenue for a single customer"""
    
    # TODO: Load actual model and make prediction
    # Simple rule-based logic for demo
    if request.monetary > 50000:
        predicted = request.monetary * 0.12
        segment = SegmentEnum.VIP
        confidence = 0.95
    elif request.monetary > 5000:
        predicted = request.monetary * 0.30
        segment = SegmentEnum.HIGH_VALUE
        confidence = 0.88
    elif request.monetary > 1000:
        predicted = request.monetary * 0.35
        segment = SegmentEnum.GROWTH
        confidence = 0.75
    else:
        predicted = request.monetary * 0.25
        segment = SegmentEnum.AT_RISK
        confidence = 0.65
    
    recommendations = [
        f"Expected 6-month revenue: £{predicted:,.0f}",
        f"Customer segment: {segment.value}",
        f"Confidence level: {confidence*100:.1f}%"
    ]
    
    return PredictionResponse(
        customerId=request.customerId,
        predictedRevenue=predicted,
        segment=segment,
        confidence=confidence,
        recommendations=recommendations
    )

@router.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):
    """Batch prediction from CSV/Excel upload"""
    
    contents = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(400, "Only CSV and Excel files supported")
        
        # Validate columns
        required_cols = ['customer_id', 'frequency', 'monetary', 'recency']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(400, f"Missing required columns: {required_cols}")
        
        # Make predictions
        predictions = []
        for _, row in df.iterrows():
            pred = await predict_revenue(PredictionRequest(
                customerId=int(row['customer_id']),
                frequency=int(row['frequency']),
                monetary=float(row['monetary']),
                recency=int(row['recency'])
            ))
            predictions.append(pred.dict())
        
        return {
            "status": "success",
            "total_predictions": len(predictions),
            "predictions": predictions
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")
