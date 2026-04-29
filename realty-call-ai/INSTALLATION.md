# RealtyCall AI - Installation & Setup Guide

## System Requirements

- **OS**: Ubuntu 20.04+, macOS 11+, or Windows 10+
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 5GB free space
- **Internet**: Stable connection required

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd realty-call-ai
```

## Step 2: Backend Setup

### 2.1 Create Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you encounter issues:

```bash
# Clear pip cache
pip cache purge

# Install with specific versions
pip install --no-cache-dir -r requirements.txt
```

### 2.3 Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your credentials
# You'll need:
# - GROQ_API_KEY: Get from https://console.groq.com
# - SARVAM_API_KEY: Get from https://www.sarvam.ai
```

## Step 3: Frontend Setup

### 3.1 Install Dependencies

```bash
cd frontend
npm install

# If you prefer yarn
yarn install
```

### 3.2 Configure Environment

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## Step 4: Running the Application

### Option A: Development Mode

**Terminal 1 - Start Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

Backend will run at: http://localhost:8000

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:3000

**Test Health Check:**
```bash
curl http://localhost:8000/health
```

### Option B: Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Step 5: Load Sample Data

### Upload Sample Properties

```bash
# Terminal 3 - Upload properties
curl -X POST "http://localhost:8000/api/properties/upload" \
  -F "file=@docs/sample_properties.json"

# Verify
curl http://localhost:8000/api/properties/count
```

### Create Test Lead

```bash
curl -X POST "http://localhost:8000/api/leads/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0000"
  }'
```

## Step 6: Testing

### 6.1 Test Chat

```bash
# In browser: http://localhost:3000
# Or via API:

curl -X POST "http://localhost:8000/api/chat/send" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "test-lead-123",
    "message": "I am looking for a 2 bedroom apartment in downtown"
  }'
```

### 6.2 API Documentation

Access interactive API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 6.3 Run Tests

```bash
cd backend

# Run pytest
pytest

# With coverage
pytest --cov=.

# Specific test file
pytest tests/test_rag.py
```

## Troubleshooting

### Backend Won't Start

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd backend
pip install -r requirements.txt --no-cache-dir
```

**Issue**: `ImportError: cannot import name 'Groq'`

**Solution**:
```bash
pip install --upgrade groq
```

### Frontend Won't Connect

**Issue**: `ECONNREFUSED 127.0.0.1:8000`

**Solution**:
1. Ensure backend is running: `curl http://localhost:8000/health`
2. Check NEXT_PUBLIC_API_URL in `.env.local`
3. Restart frontend: `npm run dev`

### FAISS Index Error

**Issue**: `RuntimeError: loaded index has 0 vectors`

**Solution**:
```bash
# Upload properties first
curl -X POST "http://localhost:8000/api/properties/upload" \
  -F "file=@docs/sample_properties.json"
```

### Database Locked Error

**Issue**: `sqlite3.OperationalError: database is locked`

**Solution**:
```bash
# Remove lock file
rm realtydb.db-journal

# Or use PostgreSQL for production
export DATABASE_URL=postgresql://user:pass@localhost/realty_db
```

### API Key Errors

**Issue**: `Authentication failed` or `Invalid API key`

**Verify**:
```bash
# Check environment variables
cat .env | grep -E "GROQ|SARVAM"

# Test Groq API
python -c "from groq import Groq; print('Groq OK')"
```

## Configuration Details

### Backend Configuration

**File**: `backend/models/config.py`

Key settings:
```python
DEBUG = True/False
LOG_LEVEL = INFO/DEBUG/WARNING
API_PORT = 8000
DATABASE_URL = sqlite:///./realtydb.db
FAISS_INDEX_PATH = ./data/property_index
```

### Frontend Configuration

**File**: `frontend/next.config.js`

Key settings:
```javascript
env: {
  NEXT_PUBLIC_API_URL: 'http://localhost:8000'
}
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature
```

### 2. Make Changes

Edit files in `backend/` or `frontend/` directories

### 3. Test Changes

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
npm run type-check
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat: description"
git push origin feature/your-feature
```

## Performance Tuning

### Backend Optimization

```python
# In .env
DEBUG=False
LOG_LEVEL=WARNING

# Database
DATABASE_URL=postgresql://user:pass@localhost/realty_db

# Caching
RAG_TOP_K=5
```

### Frontend Optimization

```bash
# Production build
npm run build
npm start

# Analyze bundle
npm run build -- --analyze
```

## Production Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for:
- Docker Compose setup
- Kubernetes deployment
- AWS/Cloud deployment
- Monitoring setup
- Backup strategy

## Getting Help

### Logs

**Backend Logs**:
```bash
tail -f logs/app.log
```

**Frontend Logs**:
- Browser DevTools: F12 → Console

### API Documentation

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Full Docs: [docs/DOCUMENTATION.md](./docs/DOCUMENTATION.md)

### Common Issues

Check [docs/DOCUMENTATION.md#troubleshooting](./docs/DOCUMENTATION.md#troubleshooting)

## Next Steps

1. ✅ Load more property data
2. ✅ Setup MCP servers (optional)
3. ✅ Configure email service
4. ✅ Setup voice pipeline
5. ✅ Deploy to production

---

**Questions?** Check DOCUMENTATION.md or open an issue on GitHub.
