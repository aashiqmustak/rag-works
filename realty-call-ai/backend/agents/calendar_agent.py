"""
Calendar Agent for scheduling meetings
"""
from datetime import datetime, timedelta
from typing import Optional
from mcp.clients import get_calendar_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CalendarAgent:
    """Calendar Agent for scheduling"""
    
    def __init__(self):
        """Initialize agent"""
        self.calendar_client = get_calendar_client()
    
    async def schedule_site_visit(self,
                                 lead_id: str,
                                 property_id: str,
                                 property_address: str,
                                 suggested_time: Optional[datetime] = None) -> Optional[str]:
        """Schedule site visit"""
        try:
            # Use suggested time or default to next available slot (2 days from now)
            if not suggested_time:
                suggested_time = datetime.now() + timedelta(days=2, hours=10)
            
            result = await self.calendar_client.schedule_meeting(
                lead_id=lead_id,
                datetime_str=suggested_time.isoformat(),
                title=f"Site Visit - {property_address}",
                duration_min=30
            )
            
            if result:
                logger.info(f"Scheduled site visit for lead {lead_id}")
                return result.get('meeting_id')
            
            return None
        
        except Exception as e:
            logger.error(f"Error scheduling site visit: {e}")
            return None
    
    async def schedule_callback(self,
                               lead_id: str,
                               preferred_time: Optional[datetime] = None) -> Optional[str]:
        """Schedule callback"""
        try:
            if not preferred_time:
                preferred_time = datetime.now() + timedelta(days=1, hours=14)
            
            result = await self.calendar_client.schedule_meeting(
                lead_id=lead_id,
                datetime_str=preferred_time.isoformat(),
                title="Follow-up Call",
                duration_min=15
            )
            
            if result:
                logger.info(f"Scheduled callback for lead {lead_id}")
                return result.get('meeting_id')
            
            return None
        
        except Exception as e:
            logger.error(f"Error scheduling callback: {e}")
            return None
    
    async def get_available_slots(self, date: str) -> Optional[list]:
        """Get available time slots"""
        try:
            result = await self.calendar_client.get_availability(date)
            if result:
                return result.get('slots', [])
            return []
        
        except Exception as e:
            logger.error(f"Error getting availability: {e}")
            return []
