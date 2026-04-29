"""
SQLAlchemy database models
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Lead(Base):
    """Lead/Customer database model"""
    __tablename__ = "leads"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    source = Column(String(50), default="voice_call")
    sales_stage = Column(String(50), default="lead")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = Column(DateTime)
    insights = Column(JSON)
    properties_viewed = Column(JSON, default=[])
    notes = Column(Text)
    
    # Relationships
    calls = relationship("Call", back_populates="lead")
    messages = relationship("Message", back_populates="lead")


class Call(Base):
    """Call record database model"""
    __tablename__ = "calls"
    
    id = Column(String(36), primary_key=True)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    duration_seconds = Column(Integer, default=0)
    transcription = Column(Text)
    summary = Column(Text)
    insights = Column(JSON)
    status = Column(String(50), default="initiated")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    recording_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="calls")


class Message(Base):
    """Chat message database model"""
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    role = Column(String(50), nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    metadata = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="messages")


class Property(Base):
    """Property listing database model"""
    __tablename__ = "properties"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    property_type = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Float)
    amenities = Column(JSON, default=[])
    images = Column(JSON, default=[])
    availability = Column(Boolean, default=True)
    agent_name = Column(String(255))
    agent_phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Meeting(Base):
    """Meeting/Site visit database model"""
    __tablename__ = "meetings"
    
    id = Column(String(36), primary_key=True)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    property_id = Column(String(36))
    meeting_type = Column(String(50))  # site_visit, broker_meeting, callback
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    location = Column(String(255))
    notes = Column(Text)
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Email(Base):
    """Email follow-up database model"""
    __tablename__ = "emails"
    
    id = Column(String(36), primary_key=True)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    properties_attached = Column(JSON, default=[])
    status = Column(String(50), default="sent")
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
