"""
Lead API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
import uuid

from models.schemas import Lead, LeadProfile, SalesStage, LeadInsight
from agents.crm_agent import CRMAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/leads", tags=["leads"])

crm_agent = CRMAgent()

# In-memory storage
leads_db: dict = {}


@router.post("/create")
async def create_lead(name: str, email: str, phone: str, source: str = "chat") -> dict:
    """Create a new lead"""
    try:
        lead_id = str(uuid.uuid4())
        
        lead_id = await crm_agent.create_lead(name, email, phone, source)
        
        leads_db[lead_id] = {
            "id": lead_id,
            "name": name,
            "email": email,
            "phone": phone,
            "source": source,
            "created_at": datetime.now(),
            "insights": None
        }
        
        return {
            "status": "success",
            "lead_id": lead_id,
            "message": f"Lead created: {name}"
        }
    
    except Exception as e:
        logger.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}")
async def get_lead(lead_id: str) -> dict:
    """Get lead details"""
    try:
        if lead_id not in leads_db:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return leads_db[lead_id]
    
    except Exception as e:
        logger.error(f"Error fetching lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{lead_id}")
async def update_lead(lead_id: str, data: dict) -> dict:
    """Update lead"""
    try:
        if lead_id not in leads_db:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        leads_db[lead_id].update(data)
        await crm_agent.update_lead(lead_id, data)
        
        return {
            "status": "success",
            "lead_id": lead_id,
            "message": "Lead updated"
        }
    
    except Exception as e:
        logger.error(f"Error updating lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{lead_id}/insights")
async def update_lead_insights(lead_id: str, insights: LeadInsight) -> dict:
    """Update lead insights"""
    try:
        if lead_id not in leads_db:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        leads_db[lead_id]["insights"] = insights.model_dump()
        
        return {
            "status": "success",
            "lead_id": lead_id,
            "insights": insights.model_dump()
        }
    
    except Exception as e:
        logger.error(f"Error updating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/stage")
async def update_sales_stage(lead_id: str, stage: str) -> dict:
    """Update sales stage"""
    try:
        if lead_id not in leads_db:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        sales_stage = SalesStage(stage)
        await crm_agent.update_sales_stage(lead_id, sales_stage)
        
        leads_db[lead_id]["sales_stage"] = stage
        
        return {
            "status": "success",
            "lead_id": lead_id,
            "sales_stage": stage
        }
    
    except Exception as e:
        logger.error(f"Error updating stage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_leads() -> dict:
    """List all leads"""
    try:
        return {
            "total": len(leads_db),
            "leads": list(leads_db.values())
        }
    
    except Exception as e:
        logger.error(f"Error listing leads: {e}")
        raise HTTPException(status_code=500, detail=str(e))
