"""
CRM Agent for lead management
"""
from datetime import datetime
from typing import Optional, Dict
from models.schemas import Lead, SalesStage
from mcp.clients import get_crm_client
from utils.logger import setup_logger
import uuid

logger = setup_logger(__name__)


class CRMAgent:
    """CRM Agent for managing leads"""
    
    def __init__(self):
        """Initialize agent"""
        self.crm_client = get_crm_client()
    
    async def create_lead(self, 
                         name: str,
                         email: str,
                         phone: str,
                         source: str = "voice_call") -> Optional[str]:
        """Create a new lead"""
        try:
            lead_id = str(uuid.uuid4())
            
            result = await self.crm_client.create_lead(
                name=name,
                email=email,
                phone=phone,
                data={
                    "id": lead_id,
                    "source": source,
                    "sales_stage": SalesStage.LEAD,
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            
            if result:
                logger.info(f"Created lead: {lead_id}")
                return lead_id
            
            return lead_id  # Return ID even if CRM sync failed
        
        except Exception as e:
            logger.error(f"Error creating lead: {e}")
            return None
    
    async def update_lead(self, 
                         lead_id: str,
                         data: Dict) -> bool:
        """Update lead information"""
        try:
            result = await self.crm_client.update_lead(lead_id, data)
            if result:
                logger.info(f"Updated lead: {lead_id}")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error updating lead: {e}")
            return False
    
    async def update_sales_stage(self, 
                                lead_id: str,
                                stage: SalesStage) -> bool:
        """Update sales stage"""
        try:
            result = await self.crm_client.update_sales_stage(lead_id, stage.value)
            if result:
                logger.info(f"Updated lead {lead_id} to stage: {stage}")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error updating sales stage: {e}")
            return False
    
    async def add_property_viewed(self, 
                                 lead_id: str,
                                 property_id: str) -> bool:
        """Add property to lead's viewed list"""
        try:
            await self.update_lead(lead_id, {
                "property_viewed": property_id,
                "updated_at": datetime.utcnow().isoformat()
            })
            return True
        
        except Exception as e:
            logger.error(f"Error adding property viewed: {e}")
            return False
