"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from models.config import settings
from utils.logger import setup_logger
from api import chat, properties, leads, calls, emails

# Setup logger
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown"""
    logger.info("🚀 RealtyCall AI Backend Starting...")
    yield
    logger.info("🛑 RealtyCall AI Backend Shutting Down...")


# Create FastAPI app
app = FastAPI(
    title="RealtyCall AI",
    description="AI-powered real estate sales call intelligence platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(properties.router)
app.include_router(leads.router)
app.include_router(calls.router)
app.include_router(emails.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RealtyCall AI Backend",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to RealtyCall AI",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "properties": "/api/properties",
            "leads": "/api/leads",
            "calls": "/api/calls",
            "emails": "/api/emails"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )
