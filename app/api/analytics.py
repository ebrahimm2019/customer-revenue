"""
Analytics API Routes
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

class SegmentSummary(BaseModel):
    segment: SegmentEnum
    count: int
    avgPredicted: float
    totalPredicted: float
    percentOfRevenue: float

@router.get("/segments", response_model=List[SegmentSummary])
async def get_segment_summary():
    """Get summary statistics for each segment"""
    
    return [
        SegmentSummary(
            segment=SegmentEnum.VIP,
            count=79,
            avgPredicted=18707,
            totalPredicted=1477860,
            percentOfRevenue=42.2
        ),
        SegmentSummary(
            segment=SegmentEnum.HIGH_VALUE,
            count=344,
            avgPredicted=2405,
            totalPredicted=827345,
            percentOfRevenue=23.6
        ),
        SegmentSummary(
            segment=SegmentEnum.GROWTH,
            count=989,
            avgPredicted=853,
            totalPredicted=843531,
            percentOfRevenue=24.1
        ),
        SegmentSummary(
            segment=SegmentEnum.AT_RISK,
            count=1117,
            avgPredicted=313,
            totalPredicted=349121,
            percentOfRevenue=10.0
        )
    ]

@router.get("/analytics/kpis")
async def get_kpis():
    """Get key performance indicators"""
    
    return {
        "totalCustomers": 2529,
        "totalPredictedRevenue": 3497857,
        "avgPredictedSpend": 1383,
        "modelAccuracy": 99.35,
        "vipCount": 79,
        "atRiskCount": 1117
    }
