# Real Estate Business - Lead Agent

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
- MCP-based CRM integrations
- Multilingual-ready architecture

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Language | Python |
| Voice Pipeline | Pipecat |
|Agent|  Agno |
| Speech-to-Text | Whisper |
| Text-to-Speech | Piper |
| LLM | Groq |
| Vector Search | FAISS |
| RAG Pipeline | Custom Python |
| MCP Integration | MCP Servers |
| Database | PostgreSQL (planned) |

---

# Architecture

```txt
User (Chat / Voice)
        ↓
FastAPI Backend
        ↓
Pipecat Voice Pipeline
        ↓
STT 
        ↓
Supervisor Agent
   ↙        ↘
RAG Agent   CRM Agent
   ↓            ↓
FAISS       MCP Servers
   ↓
LLM 
   ↓
TTS 
   ↓
Response to User
