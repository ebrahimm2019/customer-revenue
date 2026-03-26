"""
Customer API Routes - Real Data
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import numpy as np

router = APIRouter()

def get_state():
    from app.main import app_state
    return app_state

@router.get("/customers")
async def get_customers(
    segment: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "pred_3stage",
    sort_dir: str = "desc",
    limit: int = 100,
    offset: int = 0,
):
    state = get_state()
    df = state['customers'].copy()
    df.index = df.index.astype(int)

    if segment and segment != 'all':
        seg_map = {'vip': 'VIP', 'high-value': 'High Value', 'growth': 'Growth', 'at-risk': 'At Risk'}
        seg = seg_map.get(segment, segment)
        df = df[df['segment'] == seg]

    if search:
        q = search.lower()
        mask = df.index.astype(str).str.contains(q)
        mask |= df['segment'].str.lower().str.contains(q)
        df = df[mask]

    asc = sort_dir == 'asc'
    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=asc)
    else:
        df = df.sort_values('pred_3stage', ascending=False)

    total = len(df)
    df = df.iloc[offset:offset + limit]

    customers = []
    for cid, row in df.iterrows():
        trend = row.get('revenue_growth_rate', 0) * row.get('rev_90d', 0)
        customers.append({
            'id': int(cid),
            'segment': row['segment'],
            'totalSpend': round(float(row['monetary_total']), 0),
            'predicted': round(float(row['pred_3stage']), 0),
            'trend': round(float(trend), 0),
            'orders': int(row['frequency']),
            'lastPurchase': f"{int(row['recency'])}d",
            'avgOrder': round(float(row['aov']), 0),
            'recency': int(row['recency']),
            'frequency': int(row['frequency']),
            'tenure': int(row['tenure_days']),
            'uniqueProducts': int(row.get('avg_uniq_prods', 0) * row['frequency']),
            'recentSpend': round(float(row['rev_90d']), 0),
            'healthScore': float(row['health_score']),
            'healthGrade': row['health_grade'],
            'pBuy': round(float(row['p_buy']), 3),
            'actualHoldout': round(float(row['actual_holdout']), 0),
        })

    return {"customers": customers, "total": total, "offset": offset, "limit": limit}


@router.get("/customers/{customer_id}")
async def get_customer_detail(customer_id: int):
    state = get_state()
    df = state['customers']
    df.index = df.index.astype(int)

    if customer_id not in df.index:
        raise HTTPException(status_code=404, detail="Customer not found")

    row = df.loc[customer_id]
    trend = row.get('revenue_growth_rate', 0) * row.get('rev_90d', 0)

    # Feature details
    features = {
        'frequency': int(row['frequency']),
        'monetary_total': round(float(row['monetary_total']), 2),
        'recency': int(row['recency']),
        'tenure_days': int(row['tenure_days']),
        'customer_age': int(row['customer_age']),
        'aov': round(float(row['aov']), 2),
        'rev_30d': round(float(row['rev_30d']), 2),
        'rev_90d': round(float(row['rev_90d']), 2),
        'rev_180d': round(float(row['rev_180d']), 2),
        'rev_365d': round(float(row['rev_365d']), 2),
        'revenue_growth_rate': round(float(row['revenue_growth_rate']), 3),
        'revenue_trend_ratio': round(float(row['revenue_trend_ratio']), 3),
        'freq_rate': round(float(row['freq_rate']), 4),
        'maturity': round(float(row['maturity']), 4),
        'recent_ratio': round(float(row['recent_ratio']), 4),
        'avg_basket_rev': round(float(row['avg_basket_rev']), 2),
        'avg_basket_qty': round(float(row['avg_basket_qty']), 1),
        'avg_uniq_prods': round(float(row['avg_uniq_prods']), 1),
        'max_order': round(float(row['max_order']), 2),
        'order_cv': round(float(row['order_cv']), 3),
        'q4_frac': round(float(row['q4_frac']), 3),
        'weekend_ratio': round(float(row['weekend_ratio']), 3),
        'is_uk': int(row['is_uk']),
        'n_countries': int(row['n_countries']),
        'cancel_count': int(row['cancel_count']),
        'return_rate': round(float(row['return_rate']), 3),
    }

    # Recommendations based on segment
    segment = row['segment']
    recs = []
    if segment == 'VIP':
        recs = ["Assign personal account manager", "Quarterly business review",
                "Exclusive product access", "24/7 priority support"]
    elif segment == 'High Value':
        recs = ["Volume discount offer (10-15%)", "Product bundle upsell",
                "Free express shipping", "Loyalty programme enrollment"]
    elif segment == 'Growth':
        recs = ["Cross-sell campaign", "Loyalty rewards programme",
                "Product recommendations", "Engagement email series"]
    else:
        if row['recency'] > 180:
            recs = ["Win-back offer (25% discount)", "Reactivation email sequence",
                    "Customer feedback survey", "Last-chance promotion"]
        else:
            recs = ["Gentle re-engagement email", "Product update notification",
                    "Loyalty incentive offer", "Personalised recommendations"]

    # Revenue breakdown for chart
    rev_windows = {
        'Last 30 days': float(row['rev_30d']),
        'Last 90 days': float(row['rev_90d']),
        'Last 180 days': float(row['rev_180d']),
        'Last 365 days': float(row['rev_365d']),
        'Lifetime': float(row['monetary_total']),
    }

    return {
        'id': int(customer_id),
        'segment': segment,
        'totalSpend': round(float(row['monetary_total']), 0),
        'predicted': round(float(row['pred_3stage']), 0),
        'trend': round(float(trend), 0),
        'orders': int(row['frequency']),
        'lastPurchase': f"{int(row['recency'])}d",
        'avgOrder': round(float(row['aov']), 0),
        'recency': int(row['recency']),
        'healthScore': float(row['health_score']),
        'healthGrade': row['health_grade'],
        'pBuy': round(float(row['p_buy']), 3),
        'actualHoldout': round(float(row['actual_holdout']), 0),
        'features': features,
        'recommendations': recs,
        'revenueWindows': rev_windows,
    }
