"""
Pydantic models for RealtyCall AI
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


class PropertyType(str, Enum):
    """Property types"""
    APARTMENT = "apartment"
    VILLA = "villa"
    HOUSE = "house"
    COMMERCIAL = "commercial"
    LAND = "land"


class SalesStage(str, Enum):
    """Sales pipeline stages"""
    LEAD = "lead"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NEGOTIATING = "negotiating"
    SITE_VISIT_SCHEDULED = "site_visit_scheduled"
    OFFER_MADE = "offer_made"
    CLOSED = "closed"
    NOT_INTERESTED = "not_interested"


class CallStatus(str, Enum):
    """Call status"""
    INITIATED = "initiated"
    RINGING = "ringing"
    CONNECTED = "connected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class LeadInsight(BaseModel):
    """Extracted lead insights from conversation"""
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_locations: List[str] = []
    property_types: List[PropertyType] = []
    urgency: Optional[str] = None  # high, medium, low
    objections: List[str] = []
    buying_intent_score: float = Field(0.0, ge=0.0, le=1.0)
    preferred_amenities: List[str] = []
    family_size: Optional[int] = None
    move_timeline: Optional[str] = None


class PropertyListing(BaseModel):
    """Property listing model"""
    id: str
    title: str
    description: str
    price: float
    property_type: PropertyType
    location: str
    coordinates: Optional[Dict[str, float]] = None
    bedrooms: int
    bathrooms: int
    area_sqft: float
    amenities: List[str] = []
    images: List[str] = []
    availability: bool = True
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None


class LeadProfile(BaseModel):
    """Lead/Customer profile"""
    id: str
    name: str
    email: EmailStr
    phone: str
    source: str = "voice_call"  # voice_call, chat, website
    sales_stage: SalesStage = SalesStage.LEAD
    created_at: datetime
    updated_at: datetime
    last_contacted: Optional[datetime] = None
    insights: Optional[LeadInsight] = None
    properties_viewed: List[str] = []
    notes: List[str] = []


class ChatMessage(BaseModel):
    """Chat message model"""
    id: Optional[str] = None
    lead_id: str
    role: str  # user or assistant
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class CallSummary(BaseModel):
    """Call summary after completion"""
    call_id: str
    lead_id: str
    duration_seconds: int
    transcription: str
    lead_insights: LeadInsight
    properties_discussed: List[PropertyListing] = []
    follow_up_actions: List[str] = []
    call_status: CallStatus
    start_time: datetime
    end_time: datetime


class ChatRequest(BaseModel):
    """Chat endpoint request"""
    lead_id: str
    message: str
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Chat endpoint response"""
    response: str
    properties_recommended: List[PropertyListing] = []
    lead_insights: Optional[LeadInsight] = None
    action_items: List[str] = []


class VoiceCallRequest(BaseModel):
    """Voice call initiation request"""
    phone_number: str
    lead_name: str
    script: Optional[str] = None
    properties_focus: Optional[List[str]] = None


class VoiceCallResponse(BaseModel):
    """Voice call initiation response"""
    call_id: str
    status: CallStatus
    lead_id: str
    timestamp: datetime


class EmailFollowUp(BaseModel):
    """Email follow-up model"""
    recipient_email: EmailStr
    subject: str
    body: str
    properties_attached: List[PropertyListing] = []
    brochure_url: Optional[str] = None
    personalization: Dict[str, str] = {}


class MeetingSchedule(BaseModel):
    """Meeting/site visit schedule"""
    lead_id: str
    property_id: str
    meeting_type: str  # site_visit, broker_meeting, callback
    proposed_time: datetime
    duration_minutes: int = 30
    location: Optional[str] = None
    notes: Optional[str] = None


class DocumentUpload(BaseModel):
    """Document upload model"""
    file_name: str
    file_type: str  # pdf, docx, txt, json
    content: str  # Base64 encoded content


class PropertyQueryRequest(BaseModel):
    """Property search query"""
    query: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 5


class PropertyQueryResponse(BaseModel):
    """Property search response"""
    results: List[PropertyListing]
    search_query: str
    relevance_scores: List[float]


class ConversationContext(BaseModel):
    """Conversation context for agent"""
    lead_id: str
    conversation_history: List[ChatMessage]
    current_lead_insights: LeadInsight
    properties_viewed: List[PropertyListing] = []
    call_status: Optional[CallStatus] = None
    metadata: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    """Agent response model"""
    agent_name: str
    action: str
    result: Dict[str, Any]
    timestamp: datetime
