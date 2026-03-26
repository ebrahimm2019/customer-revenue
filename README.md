# Customer Revenue Intelligence Platform

A fully dynamic ML-powered web application for predicting customer revenue using a Three-Stage XGBoost model trained on the UCI Online Retail II dataset.

## What Changed: Static → Dynamic

| Feature | Before (Static) | After (Dynamic) |
|---------|-----------------|-----------------|
| Data | 10 hardcoded customers | 4,250 real customers from dataset |
| Model | Rule-based mock predictions | Three-Stage XGBoost (R²=98.56%) |
| Pages | 1 page (Customers table only) | 4 full pages (Overview, Customers, Analytics, Model) |
| Predictions | Fake multiplier logic | Real ML model with 3 stages |
| Segments | Static counts | Computed from real features |
| Charts | None | 12 interactive Chart.js visualizations |
| Search/Filter | Client-side on 10 rows | Server-side on 4,250 customers |

## Pages

### 1. Overview
- KPI dashboard (total customers, predicted revenue, model accuracy, segment counts)
- Segment summary cards with real statistics
- Monthly revenue trend (Dec 2009 – Dec 2011) with calibration/holdout split
- Revenue by country and top products charts
- Segment revenue distribution (doughnut chart)

### 2. Customers
- Full searchable, sortable, paginated customer database (4,250 customers)
- Filter by segment (VIP, High Value, Growth, At Risk)
- Click any row for detailed customer profile:
  - All 30 engineered features
  - Revenue windows chart (30d, 90d, 180d, 365d, lifetime)
  - Health score and grade
  - Purchase probability from the classifier
  - Actual vs predicted holdout revenue
  - Segment-specific recommendations

### 3. Analytics
- Feature importance (XGBoost model weights)
- Feature correlation with holdout revenue
- Revenue capture curves (4 models vs random baseline)
- Segment distribution (count + avg predicted spend)
- Data quality/cleaning summary

### 4. Model
- Full 13-model comparison table (RMSE, MAE, R², MedAE)
- RMSE and R² bar charts
- **Live Prediction Tool**: Enter customer metrics → get real-time prediction from the Three-Stage XGBoost model

## ML Pipeline

### Models Trained (13 total)
1. Naive Baseline (R²=0.33)
2. Linear Regression (R²=0.68)
3. Ridge Regression (R²=0.68)
4. Lasso Regression (R²=0.68)
5. Random Forest (R²=0.71)
6. Gradient Boosting (R²=0.99)
7. XGBoost (R²=0.98)
8. LightGBM (R²=0.91)
9. Two-Stage XGBoost (R²=0.98)
10. **Three-Stage XGBoost (R²=0.986)** ← Best MAE, used for predictions
11. XGBoost Tuned (R²=0.98)
12. LightGBM Tuned (R²=0.85)
13. Random Forest Tuned (R²=0.80)

### Three-Stage Architecture
- **Stage 1**: XGBoost Classifier → Will this customer buy? (AUC=0.978)
- **Stage 2**: XGBoost Tier Classifier → Low / Medium / High value? (Accuracy=92.3%)
- **Stage 3**: Conditional XGBoost Regressors → How much will they spend?

### 30 Engineered Features
RFM Core (5) · Temporal Windows (4) · Momentum & Trend (3) · Lifecycle (4) · Stability (2) · Product Diversity (2) · Order Characteristics (4) · Seasonality (3) · Geography (2) · Return Behaviour (2)

## Running Locally

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/customers` | GET | List customers (search, filter, sort, paginate) |
| `/api/customers/{id}` | GET | Customer detail with features |
| `/api/predict` | POST | Real-time revenue prediction |
| `/api/segments` | GET | Segment summary statistics |
| `/api/analytics/kpis` | GET | Key performance indicators |
| `/api/analytics/model-comparison` | GET | All 13 model metrics |
| `/api/analytics/monthly-revenue` | GET | 25 months of revenue data |
| `/api/analytics/feature-importance` | GET | XGBoost feature weights |
| `/api/analytics/feature-correlations` | GET | Feature-target correlations |
| `/api/analytics/revenue-capture` | GET | Revenue capture curve data |
| `/api/analytics/cleaning-summary` | GET | Data quality report |
| `/api/analytics/top-products` | GET | Top 10 products by revenue |
| `/api/analytics/country-data` | GET | Revenue by country |
| `/api/campaigns` | POST | Campaign planner with ROI |

## Tech Stack
- **Backend**: FastAPI + Python 3.11
- **ML**: XGBoost, LightGBM, scikit-learn
- **Frontend**: Vanilla HTML/CSS/JS + Chart.js
- **Design**: Dark theme, Inter font, responsive layout
