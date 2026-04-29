# Production Deployment Guide

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] Database migrations run
- [ ] Security keys rotated
- [ ] HTTPS certificates configured
- [ ] CDN setup for static assets
- [ ] Monitoring and logging configured
- [ ] Backup strategy implemented
- [ ] Load balancer configured
- [ ] Rate limiting enabled
- [ ] API documentation updated

## Environment Setup

### Production Environment Variables

```bash
# Backend
DEBUG=False
LOG_LEVEL=WARNING
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=postgresql://user:pass@db-host/realty_db

# LLM & Speech
GROQ_API_KEY=prod_key
SARVAM_API_KEY=prod_key

# Security
SECRET_KEY=generate_with_secrets.token_urlsafe(32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=https://yourdomain.com

# External Services
MCP_CRM_URL=https://crm.yourdomain.com
MCP_CALENDAR_URL=https://calendar.yourdomain.com
MCP_GMAIL_URL=https://gmail.yourdomain.com

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=app_password

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

## Deployment Strategies

### Strategy 1: Docker Compose

```bash
# Build images
docker-compose build

# Run services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Strategy 2: Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: realty-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: realty-api
  template:
    metadata:
      labels:
        app: realty-api
    spec:
      containers:
      - name: realty-api
        image: realty-call-ai-backend:prod
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: realty-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### Strategy 3: AWS ECS

```bash
# Create ECR repositories
aws ecr create-repository --repository-name realty-backend
aws ecr create-repository --repository-name realty-frontend

# Push images
docker tag realty-call-ai-backend:latest {account}.dkr.ecr.{region}.amazonaws.com/realty-backend:latest
docker push {account}.dkr.ecr.{region}.amazonaws.com/realty-backend:latest

# Deploy with CloudFormation or Terraform
```

## Performance Optimization

### Backend Optimization

```python
# Cache LLM responses
from functools import lru_cache

@lru_cache(maxsize=1000)
async def get_cached_response(query: str):
    return await llm_service.generate_response(query)

# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)

# Async context
@asynccontextmanager
async def async_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
```

### Frontend Optimization

```javascript
// Next.js Image Optimization
import Image from 'next/image';

<Image
  src="/property.jpg"
  alt="Property"
  width={600}
  height={400}
  priority
/>

// Code splitting
const ChatWindow = dynamic(() => import('@/components/ChatWindow'), {
  loading: () => <LoadingSpinner />
});
```

## Monitoring & Logging

### Sentry Integration (Backend)

```python
import sentry_sdk

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=0.1,
    environment="production"
)
```

### CloudWatch Logs

```python
import logging
import watchtower

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        watchtower.CloudWatchLogHandler()
    ]
)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram

chat_requests = Counter('chat_requests_total', 'Total chat requests')
chat_duration = Histogram('chat_duration_seconds', 'Chat response time')

@app.post("/api/chat/send")
async def send_message(request: ChatRequest):
    chat_requests.inc()
    with chat_duration.time():
        return await process_chat(request)
```

## Backup & Disaster Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump realty_db > backup_$(date +%Y%m%d).sql

# Automated daily backups
0 2 * * * pg_dump realty_db | gzip > /backups/backup_$(date +\%Y\%m\%d).sql.gz
```

### FAISS Index Backup

```bash
# Backup RAG index
cp -r data/property_index /backups/property_index_$(date +%Y%m%d)

# Restore from backup
cp -r /backups/property_index_20240101 data/property_index
```

## Scaling Considerations

### Horizontal Scaling

```yaml
# Load balancer configuration (nginx)
upstream backend {
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### Caching Layer

```python
# Redis caching
from redis import Redis
import json

redis_client = Redis(host='redis', port=6379)

async def get_cached(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

async def set_cached(key: str, value: dict, ttl: int = 3600):
    redis_client.setex(key, ttl, json.dumps(value))
```

## Security Hardening

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat/send")
@limiter.limit("10/minute")
async def send_message(request: ChatRequest):
    return await process_chat(request)
```

### Input Validation

```python
from pydantic import validator, Field

class ChatRequest(BaseModel):
    lead_id: str = Field(..., min_length=1, max_length=36)
    message: str = Field(..., min_length=1, max_length=5000)
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v
```

### HTTPS & HSTS

```python
# Add security headers
from fastapi.middleware import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com"]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

## Rollback Procedure

```bash
# Save current version
docker tag realty-backend:latest realty-backend:backup-$(date +%Y%m%d-%H%M%S)

# Rollback to previous version
docker tag realty-backend:v1.0.0 realty-backend:latest
docker-compose down
docker-compose up -d

# Monitor for errors
docker-compose logs -f
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build backend
        run: |
          cd backend
          docker build -t realty-backend:latest .
      
      - name: Build frontend
        run: |
          cd frontend
          docker build -t realty-frontend:latest .
      
      - name: Deploy
        run: docker-compose up -d
```

## Post-Deployment Verification

```bash
# Health check
curl https://api.yourdomain.com/health

# Database connection
curl https://api.yourdomain.com/health/db

# External services
curl https://api.yourdomain.com/health/services

# Performance test
ab -n 1000 -c 10 https://api.yourdomain.com/health
```

## Support & Maintenance

- Set up on-call rotation
- Document runbooks for common issues
- Regular security audits
- Monthly performance reviews
- Quarterly disaster recovery drills
