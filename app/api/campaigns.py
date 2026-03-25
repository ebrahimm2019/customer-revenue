"""
Campaigns API Routes
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from enum import Enum

router = APIRouter()

class SegmentEnum(str, Enum):
    VIP = "VIP"
    HIGH_VALUE = "High Value"
    GROWTH = "Growth"
    AT_RISK = "At Risk"

class CampaignRequest(BaseModel):
    segment: SegmentEnum
    targetCount: int = 100

class CampaignResponse(BaseModel):
    campaign_id: str
    segment: SegmentEnum
    targetCustomers: int
    estimatedCost: float
    projectedRevenue: float
    roi: float
    tactics: List[str]

@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(request: CampaignRequest):
    """Generate a targeted campaign"""
    
    campaigns = {
        "VIP": {
            "cost_per_customer": 862,
            "revenue_multiplier": 0.95,
            "tactics": [
                "Personal account manager",
                "Quarterly business review",
                "Exclusive product access",
                "24/7 priority support"
            ]
        },
        "High Value": {
            "cost_per_customer": 255,
            "revenue_multiplier": 1.15,
            "tactics": [
                "Volume discount (10-15%)",
                "Product bundles",
                "Free express shipping",
                "Loyalty rewards"
            ]
        },
        "Growth": {
            "cost_per_customer": 101,
            "revenue_multiplier": 1.25,
            "tactics": [
                "Win-back email (20% off)",
                "Cross-sell recommendations",
                "Cart abandonment recovery",
                "Referral program"
            ]
        },
        "At Risk": {
            "cost_per_customer": 31,
            "revenue_multiplier": 0.15,
            "tactics": [
                "Reactivation offer (25% off)",
                "Customer survey",
                "Automated email sequence",
                "Last-chance promotion"
            ]
        }
    }
    
    config = campaigns[request.segment.value]
    estimated_cost = request.targetCount * config['cost_per_customer']
    projected_revenue = request.targetCount * 2000 * config['revenue_multiplier']
    roi = (projected_revenue / estimated_cost - 1) * 100
    
    return CampaignResponse(
        campaign_id=f"CAMP-{request.segment.value.upper()}-20250325",
        segment=request.segment,
        targetCustomers=request.targetCount,
        estimatedCost=estimated_cost,
        projectedRevenue=projected_revenue,
        roi=roi,
        tactics=config['tactics']
    )
