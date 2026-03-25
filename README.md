# 🚀 Customer Revenue Intelligence - Railway Deployment

## 📦 What's Included

This is a **complete, production-ready** package for Railway deployment with Docker.

### Features
- ✅ Dark theme customer intelligence UI
- ✅ FastAPI backend with all endpoints
- ✅ Docker containerization
- ✅ Railway-optimized configuration
- ✅ Health checks
- ✅ CORS configured
- ✅ Mock data (replace with your database)
- ✅ API documentation (Swagger UI)

---

## 🎯 QUICK DEPLOY TO RAILWAY

### Option 1: Deploy via GitHub (Recommended)

```bash
# 1. Initialize git repository
cd railway-deploy
git init

# 2. Create repository on GitHub
# Go to github.com → New Repository → "customer-revenue-intelligence"

# 3. Push code
git add .
git commit -m "Initial commit: Customer Revenue Intelligence"
git remote add origin https://github.com/YOUR_USERNAME/customer-revenue-intelligence.git
git branch -M main
git push -u origin main

# 4. Deploy on Railway
# - Go to railway.app
# - Click "New Project"
# - Select "Deploy from GitHub repo"
# - Choose your repository
# - Railway will auto-detect Dockerfile and deploy!
```

### Option 2: Deploy via Railway CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd railway-deploy
railway init

# 4. Deploy
railway up

# 5. Get URL
railway open
```

---

## 🏗️ PROJECT STRUCTURE

```
railway-deploy/
├── Dockerfile                  # Docker configuration
├── railway.json               # Railway configuration
├── requirements.txt           # Python dependencies
├── .dockerignore             # Docker ignore rules
├── .gitignore                # Git ignore rules
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   ├── customers.py      # Customer endpoints
│   │   ├── predictions.py    # Prediction endpoints
│   │   ├── campaigns.py      # Campaign endpoints
│   │   └── analytics.py      # Analytics endpoints
│   └── static/
│       └── index.html        # Dark theme UI
├── models/
│   └── .gitkeep
├── data/
│   └── .gitkeep
└── uploads/
    └── .gitkeep
```

---

## 📋 API ENDPOINTS

Once deployed, your API will be available at:
`https://your-app.railway.app`

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main UI (dark theme table) |
| GET | `/docs` | API documentation (Swagger) |
| GET | `/api/health` | Health check |
| GET | `/api/customers` | List customers |
| GET | `/api/customers/{id}` | Customer detail |
| POST | `/api/predict` | Single prediction |
| POST | `/api/predict/batch` | Batch predictions (CSV/Excel) |
| POST | `/api/campaigns` | Create campaign |
| GET | `/api/segments` | Segment summary |
| GET | `/api/analytics/kpis` | KPIs |

---

## 🧪 TEST YOUR DEPLOYMENT

### 1. Health Check

```bash
curl https://your-app.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Customer Revenue Intelligence",
  "version": "2.0.0"
}
```

### 2. Get Customers

```bash
curl https://your-app.railway.app/api/customers
```

### 3. Get VIP Customers

```bash
curl "https://your-app.railway.app/api/customers?segment=VIP"
```

### 4. API Documentation

```
https://your-app.railway.app/docs
```

---

## 🔧 LOCAL DEVELOPMENT

### Run with Docker

```bash
# Build image
docker build -t customer-intelligence .

# Run container
docker run -p 8000:8000 customer-intelligence

# Open browser
open http://localhost:8000
```

### Run without Docker

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000

# Open browser
open http://localhost:8000
```

---

## 🗄️ DATABASE INTEGRATION

Currently uses mock data. To connect your PostgreSQL:

### 1. Add database URL to Railway

```
Railway Dashboard → Variables → Add Variable
Name: DATABASE_URL
Value: postgresql://user:password@host:port/dbname
```

### 2. Update `app/api/customers.py`

```python
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@router.get("/customers")
async def get_customers():
    # Replace MOCK_CUSTOMERS with:
    query = "SELECT * FROM customers LIMIT 100"
    customers = pd.read_sql(query, engine)
    return customers.to_dict('records')
```

---

## ⚙️ ENVIRONMENT VARIABLES

Set in Railway Dashboard → Settings → Variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Server port (Railway sets automatically) | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ❌ |
| `MODEL_PATH` | Path to trained model file | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins | ❌ |
| `API_KEY` | API authentication key | ❌ |

---

## 🎨 CUSTOMIZATION

### Change Colors

Edit `app/static/index.html`:

```css
/* VIP segment color */
.segment-badge.vip {
    color: #YOUR_COLOR;
    background: rgba(YOUR_RGB, 0.1);
}
```

### Add More Endpoints

Create new file in `app/api/`:

```python
# app/api/reports.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/reports")
async def get_reports():
    return {"reports": []}
```

Update `app/main.py`:

```python
from app.api.reports import router as reports_router
app.include_router(reports_router, prefix="/api")
```

---

## 🚨 TROUBLESHOOTING

### Issue: Build fails on Railway

**Check:**
- Dockerfile syntax is correct
- requirements.txt has no typos
- All files are committed to git

**Solution:**
```bash
# Test build locally
docker build -t test-build .

# If successful, push to Railway
git push
```

### Issue: Health check fails

**Check Railway logs:**
```
Railway Dashboard → Deployments → View Logs
```

**Common causes:**
- Port binding issue (use `$PORT` env var)
- Missing dependencies
- Python import errors

### Issue: UI doesn't load

**Check:**
- `/` endpoint returns HTML
- `app/static/index.html` exists
- Static files mounted correctly

**Solution:**
```bash
# Verify static directory
ls app/static/

# Should see: index.html
```

### Issue: CORS errors

**Update CORS in `app/main.py`:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 MONITORING

### Check Deployment Status

```
Railway Dashboard → Deployments
```

### View Logs

```
Railway Dashboard → Deployments → View Logs
```

### Railway CLI

```bash
# View logs
railway logs

# Check status
railway status

# Connect to shell
railway run bash
```

---

## 🔐 SECURITY

### Production Checklist

- [ ] Update CORS origins (don't use `["*"]`)
- [ ] Add API authentication
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (Railway does this automatically)
- [ ] Set up rate limiting
- [ ] Add input validation
- [ ] Use parameterized queries (prevent SQL injection)

### Add API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY", "your-secret-key")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(403, "Invalid API key")
    return api_key

@router.get("/customers")
async def get_customers(api_key: str = Security(verify_api_key)):
    # Protected endpoint
    pass
```

---

## 🚀 DEPLOYMENT CHECKLIST

Before deploying to production:

### Code
- [x] All files included
- [x] Dockerfile builds successfully
- [x] Requirements.txt complete
- [ ] Database connected (replace mock data)
- [ ] Model loaded (if applicable)
- [ ] Environment variables set

### Railway
- [ ] Project created
- [ ] GitHub connected
- [ ] Environment variables configured
- [ ] Custom domain added (optional)
- [ ] Health check passing

### Testing
- [ ] Health endpoint works
- [ ] API endpoints return data
- [ ] UI loads correctly
- [ ] CORS configured
- [ ] No console errors

---

## 📞 SUPPORT

### Documentation
- FastAPI docs: https://fastapi.tiangolo.com
- Railway docs: https://docs.railway.app
- Docker docs: https://docs.docker.com

### Common Commands

```bash
# Railway CLI
railway login          # Login to Railway
railway init           # Initialize project
railway up             # Deploy
railway logs           # View logs
railway run bash       # Shell access
railway link           # Link local to Railway project

# Docker
docker build -t app .  # Build image
docker run -p 8000:8000 app  # Run container
docker ps              # List containers
docker logs <id>       # View logs

# Local Development
uvicorn app.main:app --reload  # Run with auto-reload
pip install -r requirements.txt  # Install dependencies
python -m pytest       # Run tests
```

---

## 🎉 SUCCESS!

If you can access these URLs, deployment succeeded:

✅ `https://your-app.railway.app` → UI loads
✅ `https://your-app.railway.app/docs` → API docs
✅ `https://your-app.railway.app/api/health` → Returns healthy
✅ `https://your-app.railway.app/api/customers` → Returns data

**Your Customer Revenue Intelligence Platform is now live!** 🚀

---

## 📝 NEXT STEPS

1. **Connect your database** (replace mock data)
2. **Upload your trained model** (add to `models/`)
3. **Customize branding** (update colors, logo)
4. **Add authentication** (API keys, OAuth)
5. **Set up monitoring** (Railway metrics, Sentry)
6. **Configure custom domain** (Railway settings)
7. **Enable CI/CD** (auto-deploy on git push)

---

**Version:** 2.0.0  
**Last Updated:** March 25, 2026  
**Status:** ✅ Production Ready
