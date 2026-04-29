"""
Configuration management for RealtyCall AI
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # FastAPI
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # LLM
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Speech Services
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    sarvam_stt_model: str = os.getenv("SARVAM_STT_MODEL", "sarvam-2-en")
    sarvam_tts_model: str = os.getenv("SARVAM_TTS_MODEL", "sarvam-tts-en")
    
    # Voice
    pipecat_workspace_id: str = os.getenv("PIPECAT_WORKSPACE_ID", "")
    pipecat_api_key: str = os.getenv("PIPECAT_API_KEY", "")
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # MCP
    mcp_crm_url: str = os.getenv("MCP_CRM_URL", "http://localhost:8001")
    mcp_calendar_url: str = os.getenv("MCP_CALENDAR_URL", "http://localhost:8002")
    mcp_gmail_url: str = os.getenv("MCP_GMAIL_URL", "http://localhost:8003")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./realtydb.db")
    sqlalchemy_echo: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    
    # FAISS
    faiss_index_path: str = os.getenv("FAISS_INDEX_PATH", "./data/property_index")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Email
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    
    # RAG
    rag_chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
    rag_chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
    rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    
    # Calls
    max_call_duration: int = int(os.getenv("MAX_CALL_DURATION", "3600"))
    call_timeout: int = int(os.getenv("CALL_TIMEOUT", "600"))
    
    # Logging
    log_file_path: str = os.getenv("LOG_FILE_PATH", "./logs/app.log")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Features
    enable_voice_calls: bool = os.getenv("ENABLE_VOICE_CALLS", "True").lower() == "true"
    enable_chat_interface: bool = os.getenv("ENABLE_CHAT_INTERFACE", "True").lower() == "true"
    enable_email_followup: bool = os.getenv("ENABLE_EMAIL_FOLLOWUP", "True").lower() == "true"
    enable_call_recording: bool = os.getenv("ENABLE_CALL_RECORDING", "False").lower() == "true"
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
