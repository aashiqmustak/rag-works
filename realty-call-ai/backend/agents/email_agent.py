"""
Email Agent for sending follow-ups
"""
from typing import List, Optional
from models.schemas import PropertyListing
from services.email_service import get_email_service
from services.llm_service import get_llm_service
from mcp.clients import get_gmail_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailAgent:
    """Email Agent for sending follow-ups"""
    
    def __init__(self):
        """Initialize agent"""
        self.email_service = get_email_service()
        self.gmail_client = get_gmail_client()
        self.llm_service = get_llm_service()
    
    async def send_followup_email(self,
                                 lead_name: str,
                                 lead_email: str,
                                 properties: List[PropertyListing],
                                 custom_message: Optional[str] = None) -> bool:
        """Send personalized follow-up email"""
        try:
            # Generate email content
            subject = f"Your Personalized Property Recommendations"
            
            # Format properties
            properties_text = "\n".join([
                f"• {p.title} - {p.location}\n"
                f"  Price: ${p.price:,.0f} | {p.bedrooms}BR/{p.bathrooms}BA | {p.area_sqft}sqft\n"
                f"  {p.description[:100]}..."
                for p in properties[:3]
            ])
            
            body = f"""Hello {lead_name},

Thank you for your interest in real estate! Based on our conversation, 
I've selected the following properties that match your requirements:

{properties_text}

{custom_message or 'I would love to help you explore these properties further. Please let me know if you would like to schedule a site visit.'}

Looking forward to helping you find your dream property!

Best regards,
RealtyCall AI Sales Team"""
            
            # Send email
            result = await self.email_service.send_email(
                to_email=lead_email,
                subject=subject,
                body=body
            )
            
            if result:
                logger.info(f"Sent follow-up email to {lead_email}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error sending follow-up email: {e}")
            return False
    
    async def send_meeting_confirmation(self,
                                       lead_name: str,
                                       lead_email: str,
                                       property_address: str,
                                       meeting_time: str,
                                       meeting_type: str = "site_visit") -> bool:
        """Send meeting confirmation email"""
        try:
            subject = f"Meeting Confirmation - {meeting_type}"
            body = f"""Hello {lead_name},

Your {meeting_type} has been confirmed!

Details:
Property: {property_address}
Date & Time: {meeting_time}

Please contact us if you need to reschedule.

Best regards,
RealtyCall AI"""
            
            result = await self.email_service.send_email(
                to_email=lead_email,
                subject=subject,
                body=body
            )
            
            if result:
                logger.info(f"Sent confirmation email to {lead_email}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error sending confirmation email: {e}")
            return False
    
    async def send_brochure(self,
                           lead_email: str,
                           property: PropertyListing) -> bool:
        """Send property brochure"""
        try:
            subject = f"Property Brochure - {property.title}"
            body = f"""Here is the brochure for {property.title}"""
            
            result = await self.email_service.send_email(
                to_email=lead_email,
                subject=subject,
                body=body
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error sending brochure: {e}")
            return False
