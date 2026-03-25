"""
Customer API Routes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

router = APIRouter()

# ════════════════════════════════════════════════════════════════════════════
# MODELS
# ════════════════════════════════════════════════════════════════════════════

class SegmentEnum(str, Enum):
    VIP = "VIP"
    HIGH_VALUE = "High Value"
    GROWTH = "Growth"
    AT_RISK = "At Risk"

class Customer(BaseModel):
    id: int
    segment: SegmentEnum
    totalSpend: float
    predicted: float
    trend: float
    orders: int
    lastPurchase: str
    avgOrder: float
    recency: int
    frequency: int
    tenure: int
    uniqueProducts: int
    recentSpend: float
    healthScore: Optional[float] = None
    healthGrade: Optional[str] = None

class CustomerDetail(Customer):
    purchaseHistory: Optional[List[dict]] = None
    recommendations: Optional[List[str]] = None

# ════════════════════════════════════════════════════════════════════════════
# MOCK DATA (Replace with database queries)
# ════════════════════════════════════════════════════════════════════════════

MOCK_CUSTOMERS = [
    {
        "id": 14646,
        "segment": "VIP",
        "totalSpend": 384000,
        "predicted": 47000,
        "trend": -14000,
        "orders": 110,
        "lastPurchase": "3d",
        "avgOrder": 137,
        "recency": 3,
        "frequency": 110,
        "tenure": 576,
        "uniqueProducts": 766,
        "recentSpend": 56674,
        "healthScore": 95,
        "healthGrade": "A"
    },
    {
        "id": 15939,
        "segment": "High Value",
        "totalSpend": 8200,
        "predicted": 4400,
        "trend": 1100,
        "orders": 11,
        "lastPurchase": "19d",
        "avgOrder": 56,
        "recency": 19,
        "frequency": 11,
        "tenure": 213,
        "uniqueProducts": 52,
        "recentSpend": 3177,
        "healthScore": 82,
        "healthGrade": "B"
    },
    {
        "id": 14936,
        "segment": "High Value",
        "totalSpend": 7900,
        "predicted": 3000,
        "trend": 484,
        "orders": 6,
        "lastPurchase": "14d",
        "avgOrder": 24,
        "recency": 14,
        "frequency": 6,
        "tenure": 422,
        "uniqueProducts": 195,
        "recentSpend": 2060,
        "healthScore": 78,
        "healthGrade": "B"
    },
    {
        "id": 12714,
        "segment": "High Value",
        "totalSpend": 12000,
        "predicted": 2100,
        "trend": 339,
        "orders": 10,
        "lastPurchase": "18d",
        "avgOrder": 21,
        "recency": 18,
        "frequency": 10,
        "tenure": 574,
        "uniqueProducts": 376,
        "recentSpend": 1307,
        "healthScore": 85,
        "healthGrade": "A"
    },
    {
        "id": 18225,
        "segment": "High Value",
        "totalSpend": 9200,
        "predicted": 2100,
        "trend": -464,
        "orders": 19,
        "lastPurchase": "43d",
        "avgOrder": 23,
        "recency": 43,
        "frequency": 19,
        "tenure": 574,
        "uniqueProducts": 217,
        "recentSpend": 587,
        "healthScore": 72,
        "healthGrade": "B"
    },
    {
        "id": 13115,
        "segment": "Growth",
        "totalSpend": 4100,
        "predicted": 1400,
        "trend": 879,
        "orders": 7,
        "lastPurchase": "23d",
        "avgOrder": 16,
        "recency": 23,
        "frequency": 7,
        "tenure": 438,
        "uniqueProducts": 161,
        "recentSpend": 879,
        "healthScore": 68,
        "healthGrade": "C"
    },
    {
        "id": 17838,
        "segment": "Growth",
        "totalSpend": 5600,
        "predicted": 1300,
        "trend": -752,
        "orders": 11,
        "lastPurchase": "131d",
        "avgOrder": 21,
        "recency": 131,
        "frequency": 11,
        "tenure": 469,
        "uniqueProducts": 111,
        "recentSpend": 0,
        "healthScore": 45,
        "healthGrade": "C"
    },
    {
        "id": 12782,
        "segment": "Growth",
        "totalSpend": 3900,
        "predicted": 1300,
        "trend": -1100,
        "orders": 9,
        "lastPurchase": "92d",
        "avgOrder": 20,
        "recency": 92,
        "frequency": 9,
        "tenure": 358,
        "uniqueProducts": 121,
        "recentSpend": 0,
        "healthScore": 52,
        "healthGrade": "C"
    },
    {
        "id": 14934,
        "segment": "Growth",
        "totalSpend": 2400,
        "predicted": 1200,
        "trend": -829,
        "orders": 4,
        "lastPurchase": "121d",
        "avgOrder": 18,
        "recency": 121,
        "frequency": 4,
        "tenure": 280,
        "uniqueProducts": 89,
        "recentSpend": 0,
        "healthScore": 38,
        "healthGrade": "D"
    },
    {
        "id": 16241,
        "segment": "Growth",
        "totalSpend": 2700,
        "predicted": 879,
        "trend": 409,
        "orders": 8,
        "lastPurchase": "16d",
        "avgOrder": 5,
        "recency": 16,
        "frequency": 8,
        "tenure": 249,
        "uniqueProducts": 355,
        "recentSpend": 570,
        "healthScore": 64,
        "healthGrade": "C"
    }
]

# ════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════

@router.get("/customers", response_model=List[Customer])
async def get_customers(
    segment: Optional[SegmentEnum] = None,
    min_value: Optional[float] = None,
    max_recency: Optional[int] = None,
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0)
):
    """
    Get customer list with filtering and pagination
    
    - **segment**: Filter by customer segment
    - **min_value**: Minimum predicted revenue
    - **max_recency**: Maximum days since last purchase
    """
    # TODO: Replace with database query
    customers = MOCK_CUSTOMERS.copy()
    
    # Apply filters
    if segment:
        customers = [c for c in customers if c['segment'] == segment.value]
    if min_value:
        customers = [c for c in customers if c['predicted'] >= min_value]
    if max_recency:
        customers = [c for c in customers if c['recency'] <= max_recency]
    
    # Pagination
    return customers[offset:offset + limit]

@router.get("/customers/{customer_id}", response_model=CustomerDetail)
async def get_customer_detail(customer_id: int):
    """Get detailed customer information"""
    # TODO: Replace with database query
    customer = next((c for c in MOCK_CUSTOMERS if c['id'] == customer_id), None)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Add recommendations
    recommendations = []
    if customer['segment'] == 'VIP':
        recommendations = [
            "Assign personal account manager",
            "Quarterly business review",
            "Exclusive product access"
        ]
    elif customer['segment'] == 'High Value':
        recommendations = [
            "Volume discount offer (10-15%)",
            "Product bundle upsell",
            "Free express shipping"
        ]
    elif customer['segment'] == 'Growth':
        recommendations = [
            "Cross-sell campaign",
            "Loyalty rewards program",
            "Product recommendations"
        ]
    else:
        recommendations = [
            "Win-back email (20% discount)",
            "Reactivation campaign",
            "Customer feedback survey"
        ]
    
    customer['recommendations'] = recommendations
    customer['purchaseHistory'] = [
        {"date": "2025-03-22", "amount": 5420, "items": 45},
        {"date": "2025-03-15", "amount": 3210, "items": 28}
    ]
    
    return customer
