"""
MCP client wrappers for CRM, Calendar, and Gmail
"""
import httpx
from typing import Dict, Any, Optional
from models.config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPClientBase:
    """Base MCP client"""
    
    def __init__(self, base_url: str):
        """Initialize MCP client"""
        self.base_url = base_url
        self.timeout = 30
    
    async def call(self, method: str, path: str, data: Dict = None) -> Optional[Dict]:
        """Call MCP endpoint"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.base_url}{path}"
                
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url)
                else:
                    return None
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"MCP error: {response.status_code}")
                    return None
        
        except Exception as e:
            logger.error(f"MCP call error: {e}")
            return None


class CRMClient(MCPClientBase):
    """CRM MCP client"""
    
    def __init__(self):
        """Initialize CRM client"""
        super().__init__(settings.mcp_crm_url)
    
    async def create_lead(self, name: str, email: str, phone: str, 
                         data: Dict = None) -> Optional[Dict]:
        """Create lead"""
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            **(data or {})
        }
        return await self.call("POST", "/leads", payload)
    
    async def update_lead(self, lead_id: str, data: Dict) -> Optional[Dict]:
        """Update lead"""
        return await self.call("PUT", f"/leads/{lead_id}", data)
    
    async def get_lead(self, lead_id: str) -> Optional[Dict]:
        """Get lead details"""
        return await self.call("GET", f"/leads/{lead_id}")
    
    async def update_sales_stage(self, lead_id: str, stage: str) -> Optional[Dict]:
        """Update sales stage"""
        return await self.call("PUT", f"/leads/{lead_id}/stage", {"stage": stage})


class CalendarClient(MCPClientBase):
    """Calendar MCP client"""
    
    def __init__(self):
        """Initialize calendar client"""
        super().__init__(settings.mcp_calendar_url)
    
    async def schedule_meeting(self, lead_id: str, datetime_str: str,
                              title: str, duration_min: int = 30) -> Optional[Dict]:
        """Schedule meeting"""
        payload = {
            "lead_id": lead_id,
            "datetime": datetime_str,
            "title": title,
            "duration_minutes": duration_min
        }
        return await self.call("POST", "/meetings", payload)
    
    async def cancel_meeting(self, meeting_id: str) -> Optional[Dict]:
        """Cancel meeting"""
        return await self.call("DELETE", f"/meetings/{meeting_id}")
    
    async def get_availability(self, date: str) -> Optional[Dict]:
        """Get availability"""
        return await self.call("GET", f"/availability?date={date}")


class GmailClient(MCPClientBase):
    """Gmail MCP client"""
    
    def __init__(self):
        """Initialize Gmail client"""
        super().__init__(settings.mcp_gmail_url)
    
    async def send_email(self, to: str, subject: str, body: str,
                        attachments: list = None) -> Optional[Dict]:
        """Send email"""
        payload = {
            "to": to,
            "subject": subject,
            "body": body,
            "attachments": attachments or []
        }
        return await self.call("POST", "/send", payload)
    
    async def send_with_template(self, to: str, template_id: str,
                                variables: Dict) -> Optional[Dict]:
        """Send email with template"""
        payload = {
            "to": to,
            "template_id": template_id,
            "variables": variables
        }
        return await self.call("POST", "/send-template", payload)


# Global MCP client instances
_crm_client = None
_calendar_client = None
_gmail_client = None


def get_crm_client() -> CRMClient:
    """Get or create CRM client"""
    global _crm_client
    if _crm_client is None:
        _crm_client = CRMClient()
    return _crm_client


def get_calendar_client() -> CalendarClient:
    """Get or create calendar client"""
    global _calendar_client
    if _calendar_client is None:
        _calendar_client = CalendarClient()
    return _calendar_client


def get_gmail_client() -> GmailClient:
    """Get or create Gmail client"""
    global _gmail_client
    if _gmail_client is None:
        _gmail_client = GmailClient()
    return _gmail_client
