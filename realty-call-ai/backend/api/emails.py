"""
Email API endpoints
"""
from fastapi import APIRouter, HTTPException
import uuid

from models.schemas import EmailFollowUp
from agents.email_agent import EmailAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/emails", tags=["emails"])

email_agent = EmailAgent()


@router.post("/send-followup")
async def send_followup(email: EmailFollowUp) -> dict:
    """Send follow-up email"""
    try:
        success = await email_agent.send_followup_email(
            lead_name="",  # Get from context
            lead_email=email.recipient_email,
            properties=email.properties_attached
        )
        
        return {
            "status": "success" if success else "failed",
            "email_id": str(uuid.uuid4()),
            "recipient": email.recipient_email,
            "subject": email.subject
        }
    
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-confirmation")
async def send_confirmation(lead_name: str, 
                          lead_email: str,
                          property_address: str,
                          meeting_time: str) -> dict:
    """Send meeting confirmation"""
    try:
        success = await email_agent.send_meeting_confirmation(
            lead_name=lead_name,
            lead_email=lead_email,
            property_address=property_address,
            meeting_time=meeting_time
        )
        
        return {
            "status": "success" if success else "failed",
            "email_id": str(uuid.uuid4()),
            "recipient": lead_email,
            "type": "confirmation"
        }
    
    except Exception as e:
        logger.error(f"Error sending confirmation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
