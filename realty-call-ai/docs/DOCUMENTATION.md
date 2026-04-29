# RealtyCall AI Documentation

## Overview

RealtyCall AI is a production-ready AI-powered real estate sales call intelligence platform that combines:

- **Voice Pipeline**: Pipecat for handling inbound/outbound calls
- **AI Intelligence**: Groq LLM for conversation understanding
- **Speech Services**: Sarvam AI for STT/TTS
- **RAG System**: FAISS-based vector search for property retrieval
- **MCP Integrations**: CRM, Calendar, and Gmail management
- **Multi-Agent Architecture**: Specialized agents for different tasks

## Quick Start

### Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run FastAPI server
python main.py
```

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run Next.js dev server
npm run dev
```

## Architecture

### Backend Structure

```
backend/
├── agents/              # AI agents for different tasks
│   ├── supervisor_agent.py      # Orchestrates all agents
│   ├── rag_agent.py             # Property retrieval
│   ├── lead_intelligence_agent.py # Lead data extraction
│   ├── crm_agent.py             # Lead management
│   ├── calendar_agent.py        # Scheduling
│   └── email_agent.py           # Email automation
├── rag/                # RAG pipeline
│   └── pipeline.py              # FAISS indexing and search
├── mcp/                # MCP client wrappers
│   └── clients.py               # CRM, Calendar, Gmail clients
├── services/           # External service integrations
│   ├── llm_service.py           # Groq LLM
│   ├── speech_service.py        # Sarvam AI STT/TTS
│   └── email_service.py         # Email sending
├── api/                # FastAPI endpoints
│   ├── chat.py                  # Chat endpoints
│   ├── properties.py            # Property endpoints
│   ├── leads.py                 # Lead endpoints
│   ├── calls.py                 # Voice call endpoints
│   └── emails.py                # Email endpoints
├── models/             # Database and Pydantic models
│   ├── schemas.py               # Pydantic schemas
│   ├── config.py                # Configuration
│   └── models.py                # Database models
├── database/           # Database layer
│   └── models.py                # SQLAlchemy models
└── main.py             # FastAPI application
```

### Frontend Structure

```
frontend/
├── app/                # Next.js app directory
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/         # React components
│   ├── ChatWindow.tsx
│   ├── ChatInput.tsx
│   ├── PropertyCard.tsx
│   ├── LeadInsightPanel.tsx
│   └── InitialLeadForm.tsx
├── services/           # API integration
│   └── api.ts
├── hooks/              # Custom React hooks
│   └── useChat.ts
├── store/              # Zustand state management
│   └── index.ts
└── types/              # TypeScript types
    └── index.ts
```

## API Endpoints

### Chat Endpoints

```bash
POST /api/chat/send
# Send a message
{
  "lead_id": "string",
  "message": "string"
}

GET /api/chat/history/{lead_id}
# Get chat history

DELETE /api/chat/history/{lead_id}
# Clear chat history
```

### Property Endpoints

```bash
POST /api/properties/search
# Search properties by query
{
  "query": "string",
  "filters": {},
  "top_k": 5
}

POST /api/properties/filter
# Filter properties by criteria

POST /api/properties/add
# Add property to index

POST /api/properties/upload
# Upload properties from JSON file

GET /api/properties/count
# Get total property count
```

### Lead Endpoints

```bash
POST /api/leads/create
# Create new lead
?name=string&email=string&phone=string&source=string

GET /api/leads/{lead_id}
# Get lead details

PUT /api/leads/{lead_id}
# Update lead

PUT /api/leads/{lead_id}/insights
# Update lead insights

POST /api/leads/{lead_id}/stage
# Update sales stage

GET /api/leads
# List all leads
```

### Call Endpoints

```bash
POST /api/calls/initiate
# Start outbound call
{
  "phone_number": "string",
  "lead_name": "string",
  "script": "string",
  "properties_focus": ["string"]
}

GET /api/calls/{call_id}
# Get call status

POST /api/calls/{call_id}/end
# End call and save summary

GET /api/calls
# List all calls
```

### Email Endpoints

```bash
POST /api/emails/send-followup
# Send follow-up email

POST /api/emails/send-confirmation
# Send meeting confirmation
```

## Configuration

### Environment Variables

Create `.env` file in backend:

```env
# FastAPI
DEBUG=True
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# LLM (Groq)
GROQ_API_KEY=your_key

# Speech (Sarvam AI)
SARVAM_API_KEY=your_key
SARVAM_STT_MODEL=sarvam-2-en
SARVAM_TTS_MODEL=sarvam-tts-en

# MCP URLs
MCP_CRM_URL=http://localhost:8001
MCP_CALENDAR_URL=http://localhost:8002
MCP_GMAIL_URL=http://localhost:8003

# Database
DATABASE_URL=sqlite:///./realtydb.db

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASSWORD=your_password

# Security
SECRET_KEY=your_secret_key
```

## Agent System

### Supervisor Agent

Orchestrates all other agents and routes tasks intelligently.

### RAG Agent

Retrieves property listings using semantic search with FAISS.

### Lead Intelligence Agent

Extracts from conversations:
- Budget range
- Preferred locations
- Property types
- Urgency level
- Objections
- Buying intent score

### CRM Agent

Manages leads through MCP integration with CRM system.

### Calendar Agent

Schedules site visits and meetings through MCP integration.

### Email Agent

Sends personalized follow-ups and confirmations.

## RAG Pipeline

Uses FAISS for efficient similarity search:

1. **Embedding**: Convert properties and queries to embeddings using SentenceTransformers
2. **Indexing**: Store embeddings in FAISS index
3. **Search**: Retrieve top-k similar properties
4. **Filtering**: Support for attribute-based filtering

```python
from rag.pipeline import get_rag_pipeline

rag = get_rag_pipeline()

# Search by query
properties, scores = rag.search("2 bedroom apartment in downtown", top_k=5)

# Search by filters
properties = rag.search_by_filters({
    'min_price': 200000,
    'max_price': 500000,
    'location': 'downtown'
})
```

## MCP Integration

MCP (Model Context Protocol) wrappers for external services:

```python
from mcp.clients import get_crm_client, get_calendar_client, get_gmail_client

# CRM
crm = get_crm_client()
await crm.create_lead("John Doe", "john@example.com", "+1234567890")
await crm.update_sales_stage(lead_id, "negotiating")

# Calendar
calendar = get_calendar_client()
await calendar.schedule_meeting(lead_id, datetime.isoformat(), "Site Visit", 30)

# Gmail
gmail = get_gmail_client()
await gmail.send_email("john@example.com", "Subject", "Body")
```

## Sample Data

### Sample Property

```json
{
  "id": "prop-001",
  "title": "Luxury Downtown Apartment",
  "description": "Modern 2BR apartment with city views",
  "price": 450000,
  "property_type": "apartment",
  "location": "Downtown District",
  "coordinates": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "bedrooms": 2,
  "bathrooms": 2,
  "area_sqft": 1200,
  "amenities": ["parking", "gym", "pool", "concierge"],
  "images": ["image1.jpg", "image2.jpg"],
  "availability": true,
  "agent_name": "Jane Smith",
  "agent_phone": "+1-555-0123"
}
```

## Deployment

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure real database (PostgreSQL/MySQL)
- [ ] Setup API authentication
- [ ] Enable HTTPS
- [ ] Setup monitoring and logging
- [ ] Configure proper CORS
- [ ] Setup backup strategy
- [ ] Configure MCP server connections
- [ ] Load production property database
- [ ] Setup CI/CD pipeline

## Performance Optimization

1. **FAISS**: Optimized vector search for large property databases
2. **Async Processing**: All I/O operations are async
3. **Caching**: Cache embeddings and search results
4. **Connection Pooling**: Reuse HTTP connections
5. **Rate Limiting**: Implement rate limits on API endpoints

## Security Considerations

1. **API Keys**: All external API keys stored in environment variables
2. **Database**: Use encrypted database connections
3. **Authentication**: Implement JWT-based authentication
4. **CORS**: Configure CORS for specific origins
5. **Input Validation**: All inputs validated with Pydantic
6. **HTTPS**: Use HTTPS in production

## Troubleshooting

### Common Issues

1. **FAISS Index Not Found**
   - Solution: Upload properties first via `/api/properties/upload`

2. **MCP Connection Errors**
   - Check if MCP servers are running
   - Verify URLs in environment variables

3. **API Key Errors**
   - Verify all API keys are correctly set
   - Check API key permissions

4. **Chat Messages Not Returning**
   - Ensure lead exists
   - Check GROQ_API_KEY is set

## Future Enhancements

- [ ] Real-time voice call transcription
- [ ] Video property tours
- [ ] ML-based lead scoring
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] WhatsApp integration
- [ ] Automated SMS follow-ups
