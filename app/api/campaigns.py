"""
Campaigns API Routes - Real Data
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

router = APIRouter()

def get_state():
    from app.main import app_state
    return app_state

class CampaignRequest(BaseModel):
    segment: str
    targetCount: int = 100

class CampaignResponse(BaseModel):
    campaign_id: str
    segment: str
    targetCustomers: int
    estimatedCost: float
    projectedRevenue: float
    roi: float
    tactics: List[str]
    segmentStats: dict

@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(request: CampaignRequest):
    state = get_state()
    df = state['customers']
    seg_data = df[df['segment'] == request.segment]

    avg_pred = float(seg_data['pred_3stage'].mean()) if len(seg_data) > 0 else 500
    actual_count = len(seg_data)
    target = min(request.targetCount, actual_count)

    # Cost & ROI based on real segment data
    configs = {
        'VIP': {'cost_mult': 0.05, 'lift': 0.10, 'tactics': [
            "Personal account manager assignment",
            "Quarterly business review scheduling",
            "Exclusive early product access",
            "24/7 priority support line",
            "Custom volume pricing negotiation",
        ]},
        'High Value': {'cost_mult': 0.08, 'lift': 0.15, 'tactics': [
            "Volume discount offer (10-15%)",
            "Product bundle upsell campaign",
            "Free express shipping for 3 months",
            "Loyalty rewards programme enrollment",
            "Cross-category recommendations",
        ]},
        'Growth': {'cost_mult': 0.10, 'lift': 0.20, 'tactics': [
            "Personalised product recommendations",
            "Loyalty reward points programme",
            "Cross-sell email campaign",
            "Free shipping threshold reduction",
            "Seasonal promotional offers",
        ]},
        'At Risk': {'cost_mult': 0.03, 'lift': 0.05, 'tactics': [
            "Win-back offer (25% discount)",
            "Reactivation email sequence (6 emails)",
            "Customer feedback survey",
            "Last-chance promotion",
            "Personalised 'We miss you' message",
        ]},
    }

    config = configs.get(request.segment, configs['Growth'])
    estimated_cost = target * avg_pred * config['cost_mult']
    projected_revenue = target * avg_pred * (1 + config['lift'])
    roi = ((projected_revenue - estimated_cost) / max(estimated_cost, 1)) * 100

    return CampaignResponse(
        campaign_id=f"CAMP-{request.segment.upper().replace(' ', '-')}-2026",
        segment=request.segment,
        targetCustomers=target,
        estimatedCost=round(estimated_cost, 0),
        projectedRevenue=round(projected_revenue, 0),
        roi=round(roi, 1),
        tactics=config['tactics'],
        segmentStats={
            'totalInSegment': actual_count,
            'avgPredicted': round(avg_pred, 0),
            'avgRecency': round(float(seg_data['recency'].mean()), 0) if len(seg_data) > 0 else 0,
            'avgFrequency': round(float(seg_data['frequency'].mean()), 1) if len(seg_data) > 0 else 0,
        }
    )
