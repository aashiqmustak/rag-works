# Real Estate Lead Agent

AI-powered real estate sales call intelligence platform that automates outbound property sales conversations using voice AI, RAG, MCP integrations, and multi-agent workflows.

The platform supports both voice calls and chat-based interactions to help real estate businesses qualify leads, recommend properties, handle objections, generate follow-ups, and improve sales conversion rates.

---

# Features

- AI outbound sales calling
- Real-time voice conversations
- Chat support interface
- Property recommendation using RAG
- Buyer intent extraction
- Call transcription and summaries
- Lead qualification
- Objection handling
- Follow-up generation
- CRM integration using MCP
- Calendar scheduling using MCP
- Gmail integration using MCP
- Multilingual-ready architecture

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Language | Python |
| Voice Pipeline | Pipecat |
| Speech-to-Text | Whisper |
| Text-to-Speech | Piper |
| LLM | Groq |
| Vector Search | FAISS |
| RAG Pipeline | Agno |
| MCP Integration | MCP Servers |
| Database | PostgreSQL |

---

# MCP Integrations

| MCP Server | Purpose |
|---|---|
| CRM MCP | Manage leads, follow-ups, customer notes, and sales stages |
| Calendar MCP | Schedule site visits, broker meetings, and callbacks |
| Gmail MCP | Send follow-up emails, brochures, and meeting confirmations |

---

# Architecture

```txt
User (Chat / Voice)
        ↓
FastAPI Backend
        ↓
Pipecat Voice Pipeline
        ↓
STT (Sarvam)
        ↓
Supervisor Agent
   ↙        ↓        ↘
RAG Agent  CRM Agent  Email Agent
   ↓            ↓            ↓
FAISS      CRM MCP    Gmail MCP
   ↓            ↓
LLM      Calendar MCP
   ↓
TTS (Sarvam)
   ↓
Response to User
