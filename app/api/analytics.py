"""
Analytics API Routes - Real Data
"""
from fastapi import APIRouter
import numpy as np

router = APIRouter()

def get_state():
    from app.main import app_state
    return app_state

@router.get("/segments")
async def get_segment_summary():
    state = get_state()
    seg = state.get('segment_summary', {})
    total_pred = sum(s['total_predicted'] for s in seg.values())
    result = []
    for name, data in seg.items():
        result.append({
            'segment': name,
            'count': data['count'],
            'avgPredicted': round(data['avg_predicted'], 0),
            'totalPredicted': round(data['total_predicted'], 0),
            'percentOfRevenue': round(data['total_predicted'] / total_pred * 100, 1) if total_pred > 0 else 0,
            'avgSpend': round(data['avg_spend'], 0),
            'avgRecency': round(data['avg_recency'], 0),
            'avgFrequency': round(data['avg_frequency'], 1),
        })
    return result

@router.get("/analytics/kpis")
async def get_kpis():
    state = get_state()
    df = state['customers']
    model_results = state.get('model_results', {})

    # Get best model R2
    best_r2 = 0
    best_model = ""
    for name, r in model_results.items():
        if r['R2'] > best_r2:
            best_r2 = r['R2']
            best_model = name

    seg_counts = df['segment'].value_counts().to_dict()

    return {
        'totalCustomers': len(df),
        'totalPredictedRevenue': round(float(df['pred_3stage'].sum()), 0),
        'avgPredictedSpend': round(float(df['pred_3stage'].mean()), 0),
        'modelR2': round(best_r2 * 100, 2),
        'bestModel': best_model,
        'bestRMSE': round(model_results.get(best_model, {}).get('RMSE', 0), 0),
        'bestMAE': round(model_results.get(best_model, {}).get('MAE', 0), 0),
        'vipCount': seg_counts.get('VIP', 0),
        'highValueCount': seg_counts.get('High Value', 0),
        'growthCount': seg_counts.get('Growth', 0),
        'atRiskCount': seg_counts.get('At Risk', 0),
        'zeroSpenderPct': round(float((df['actual_holdout'] == 0).mean() * 100), 1),
        'activeBuyerPct': round(float((df['actual_holdout'] > 0).mean() * 100), 1),
        'medianPrediction': round(float(df['pred_3stage'].median()), 0),
        'totalActualRevenue': round(float(df['actual_holdout'].sum()), 0),
    }

@router.get("/analytics/model-comparison")
async def get_model_comparison():
    state = get_state()
    return state.get('model_results', {})

@router.get("/analytics/monthly-revenue")
async def get_monthly_revenue():
    state = get_state()
    df = state.get('monthly_revenue')
    if df is None:
        return []
    records = df.to_dict('records')
    for r in records:
        r['revenue'] = round(r['revenue'], 0)
    return records

@router.get("/analytics/feature-importance")
async def get_feature_importance():
    state = get_state()
    df = state.get('feature_importance')
    if df is None:
        return []
    df = df.copy()
    # CSV has unnamed index col + value col
    if len(df.columns) == 2:
        df.columns = ['feature', 'importance']
    elif len(df.columns) == 1:
        df = df.reset_index()
        df.columns = ['feature', 'importance']
    return df.head(15).to_dict('records')

@router.get("/analytics/feature-correlations")
async def get_feature_correlations():
    state = get_state()
    df = state.get('feature_correlations')
    if df is None:
        return []
    df = df.copy()
    if len(df.columns) == 2:
        df.columns = ['feature', 'correlation']
    elif len(df.columns) == 1:
        df = df.reset_index()
        df.columns = ['feature', 'correlation']
    return df.head(15).to_dict('records')

@router.get("/analytics/revenue-capture")
async def get_revenue_capture():
    state = get_state()
    return state.get('revenue_capture', {})

@router.get("/analytics/cleaning-summary")
async def get_cleaning_summary():
    state = get_state()
    return state.get('cleaning_summary', {})

@router.get("/analytics/top-products")
async def get_top_products():
    state = get_state()
    df = state.get('top_products')
    if df is None:
        return []
    df = df.copy()
    # Handle different column name formats
    if 'Description' in df.columns:
        df = df.rename(columns={'Description': 'product'})
    elif df.index.name == 'Description':
        df = df.reset_index().rename(columns={'Description': 'product'})
    col_map = {c: c.lower() for c in df.columns}
    df = df.rename(columns=col_map)
    if 'product' not in df.columns and len(df.columns) >= 4:
        df.columns = ['product', 'revenue', 'qty', 'orders']
    return df.head(10).to_dict('records')

@router.get("/analytics/country-data")
async def get_country_data():
    state = get_state()
    df = state.get('country_data')
    if df is None:
        return []
    df = df.copy()
    if 'Country' in df.columns:
        df = df.rename(columns={'Country': 'country'})
    elif df.index.name == 'Country':
        df = df.reset_index().rename(columns={'Country': 'country'})
    col_map = {c: c.lower() for c in df.columns}
    df = df.rename(columns=col_map)
    if 'country' not in df.columns and len(df.columns) >= 4:
        df.columns = ['country', 'revenue', 'customers', 'orders']
    return df.to_dict('records')
