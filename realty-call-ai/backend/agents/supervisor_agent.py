"""
Supervisor Agent - coordinates all other agents
"""
from typing import List, Dict, Optional
from datetime import datetime
from models.schemas import (
    ChatMessage, LeadInsight, PropertyListing, 
    ConversationContext, CallStatus
)
from agents.rag_agent import RAGAgent
from agents.lead_intelligence_agent import LeadIntelligenceAgent
from agents.crm_agent import CRMAgent
from agents.calendar_agent import CalendarAgent
from agents.email_agent import EmailAgent
from services.llm_service import get_llm_service
from prompts.agent_prompts import SUPERVISOR_SYSTEM_PROMPT
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SupervisorAgent:
    """Supervisor Agent - orchestrates all other agents"""
    
    def __init__(self):
        """Initialize supervisor and all agents"""
        self.rag_agent = RAGAgent()
        self.lead_agent = LeadIntelligenceAgent()
        self.crm_agent = CRMAgent()
        self.calendar_agent = CalendarAgent()
        self.email_agent = EmailAgent()
        self.llm_service = get_llm_service()
    
    async def process_message(self,
                             user_message: str,
                             context: ConversationContext) -> Dict:
        """Process user message and coordinate agent responses"""
        try:
            # Prepare conversation history
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in context.conversation_history[-10:]  # Last 10 messages
            ]
            messages.append({"role": "user", "content": user_message})
            
            # Extract lead insights
            insights = await self.lead_agent.extract_insights(messages)
            if insights:
                context.current_lead_insights = insights
            
            # Search for properties based on context
            properties = []
            if context.current_lead_insights:
                query = self._build_search_query(context.current_lead_insights)
                properties = await self.rag_agent.search_properties(
                    query=query,
                    filters=self._build_filters(context.current_lead_insights)
                )
                context.properties_viewed.extend(properties)
            
            # Generate supervisor response
            response = await self.llm_service.generate_response(
                messages=messages,
                system_prompt=SUPERVISOR_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=512
            )
            
            # Format response with properties
            if properties:
                response += f"\n\n📍 Found {len(properties)} properties matching your criteria"
            
            # Update CRM if this is a new lead
            if not context.lead_id:
                # Extract name and contact if available
                contact_info = self._extract_contact_info(user_message)
                if contact_info:
                    lead_id = await self.crm_agent.create_lead(
                        name=contact_info.get('name', 'Unknown'),
                        email=contact_info.get('email', 'unknown@example.com'),
                        phone=contact_info.get('phone', 'unknown'),
                        source='chat'
                    )
                    if lead_id:
                        context.lead_id = lead_id
            
            return {
                "response": response,
                "properties": properties,
                "insights": insights,
                "action_items": []
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": "I encountered an error. Could you please try again?",
                "properties": [],
                "insights": None,
                "action_items": []
            }
    
    def _build_search_query(self, insights: LeadInsight) -> str:
        """Build search query from insights"""
        parts = []
        
        if insights.preferred_locations:
            parts.append(f"location:{','.join(insights.preferred_locations)}")
        
        if insights.property_types:
            parts.append(f"type:{','.join([t.value for t in insights.property_types])}")
        
        if insights.preferred_amenities:
            parts.append(f"amenities:{','.join(insights.preferred_amenities)}")
        
        if insights.budget_min or insights.budget_max:
            budget_str = f"{insights.budget_min or 'any'}-{insights.budget_max or 'any'}"
            parts.append(f"budget:{budget_str}")
        
        return " ".join(parts) if parts else "residential property"
    
    def _build_filters(self, insights: LeadInsight) -> Dict:
        """Build filter dict from insights"""
        filters = {}
        
        if insights.budget_min:
            filters['min_price'] = insights.budget_min
        
        if insights.budget_max:
            filters['max_price'] = insights.budget_max
        
        if insights.preferred_locations:
            filters['location'] = insights.preferred_locations[0]
        
        if insights.property_types:
            filters['property_type'] = insights.property_types[0].value
        
        return filters
    
    def _extract_contact_info(self, message: str) -> Optional[Dict]:
        """Try to extract contact info from message"""
        # Simple extraction - in production, use NER or similar
        import re
        
        info = {}
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if email_match:
            info['email'] = email_match.group()
        
        # Phone
        phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', message)
        if phone_match:
            info['phone'] = phone_match.group()
        
        # Name (basic)
        if len(info) > 0:
            return info
        
        return None
