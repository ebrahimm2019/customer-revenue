"""
Predictions API Routes - Real Model Integration
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import pandas as pd

router = APIRouter()

def get_state():
    from app.main import app_state
    return app_state

class PredictionRequest(BaseModel):
    frequency: int
    monetary_total: float
    recency: int
    tenure_days: int = 180
    rev_30d: float = 0
    rev_90d: float = 0
    rev_180d: float = 0
    rev_365d: float = 0
    n_orders: int = 1
    avg_basket_rev: float = 0
    avg_basket_qty: float = 10
    avg_uniq_prods: float = 5
    customer_age: int = 180
    is_uk: int = 1

class PredictionResponse(BaseModel):
    predictedRevenue: float
    purchaseProbability: float
    segment: str
    tier: str
    confidence: str
    recommendations: List[str]

@router.post("/predict", response_model=PredictionResponse)
async def predict_revenue(request: PredictionRequest):
    """Predict 6-month revenue using the Three-Stage XGBoost model"""
    state = get_state()
    model = state.get('model')
    if not model:
        raise HTTPException(500, "Model not loaded")

    feature_names = model['feature_names']

    # Build feature vector with defaults for missing features
    features = {fn: 0.0 for fn in feature_names}
    features['frequency'] = request.frequency
    features['monetary_total'] = request.monetary_total
    features['recency'] = request.recency
    features['tenure_days'] = request.tenure_days
    features['customer_age'] = request.customer_age
    features['aov'] = request.monetary_total / max(request.frequency, 1)
    features['rev_30d'] = request.rev_30d
    features['rev_90d'] = request.rev_90d
    features['rev_180d'] = request.rev_180d
    features['rev_365d'] = request.rev_365d
    features['n_orders'] = request.n_orders
    features['n_purchase_days'] = request.frequency
    features['n_orders_items'] = int(request.avg_basket_qty * request.frequency)
    features['avg_basket_rev'] = request.avg_basket_rev if request.avg_basket_rev > 0 else features['aov']
    features['avg_basket_qty'] = request.avg_basket_qty
    features['avg_uniq_prods'] = request.avg_uniq_prods
    features['max_order'] = request.monetary_total / max(request.frequency, 1) * 1.5
    features['freq_rate'] = request.frequency / max(request.tenure_days, 1)
    features['maturity'] = request.frequency / max(request.customer_age, 1)
    features['recent_ratio'] = request.rev_90d / max(request.monetary_total, 1)
    features['is_uk'] = request.is_uk
    features['n_countries'] = 1

    # Revenue growth
    if request.rev_90d > 0 and request.rev_180d > request.rev_90d:
        prev_90 = request.rev_180d - request.rev_90d
        features['revenue_growth_rate'] = (request.rev_90d - prev_90) / max(prev_90, 1)
        features['revenue_trend_ratio'] = (request.rev_90d + 1) / max(prev_90 + 1, 1)

    X = pd.DataFrame([features])[feature_names]

    # Stage 1: Purchase probability
    clf = model['classifier']
    p_buy = float(clf.predict_proba(X)[0, 1])

    # Stage 2: Tier classification
    tier_clf = model['tier_classifier']
    pred_tier = int(tier_clf.predict(X)[0])
    tier_names = {0: 'Low', 1: 'Medium', 2: 'High'}

    # Stage 3: Conditional regression
    tier_reg = model['tier_regressors'][pred_tier]
    raw_pred = float(tier_reg.predict(X)[0])
    predicted = max(p_buy * max(raw_pred, 0), 0)

    # Segment assignment
    if predicted > 5000 or request.monetary_total > 10000:
        segment = 'VIP'
    elif predicted > 1500 or request.monetary_total > 3000:
        segment = 'High Value'
    elif p_buy > 0.3:
        segment = 'Growth'
    else:
        segment = 'At Risk'

    # Confidence
    if p_buy > 0.8:
        confidence = 'High'
    elif p_buy > 0.5:
        confidence = 'Medium'
    else:
        confidence = 'Low'

    # Recommendations
    recs = [f"Predicted 6-month revenue: £{predicted:,.0f}",
            f"Purchase probability: {p_buy*100:.0f}%",
            f"Customer tier: {tier_names[pred_tier]} value"]

    if segment == 'VIP':
        recs.append("Assign dedicated account manager")
    elif segment == 'High Value':
        recs.append("Offer volume discounts to increase order size")
    elif segment == 'Growth':
        recs.append("Cross-sell campaign recommended")
    else:
        recs.append("Reactivation campaign with 20% discount")

    return PredictionResponse(
        predictedRevenue=round(predicted, 2),
        purchaseProbability=round(p_buy, 4),
        segment=segment,
        tier=tier_names[pred_tier],
        confidence=confidence,
        recommendations=recs,
    )
