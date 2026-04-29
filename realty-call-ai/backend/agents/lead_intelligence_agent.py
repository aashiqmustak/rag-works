"""
Lead Intelligence Agent for extracting insights from conversations
"""
import json
from typing import Optional
from models.schemas import LeadInsight, PropertyType
from services.llm_service import get_llm_service
from prompts.agent_prompts import LEAD_INTELLIGENCE_PROMPT
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LeadIntelligenceAgent:
    """Extracts lead intelligence from conversations"""
    
    def __init__(self):
        """Initialize agent"""
        self.llm_service = get_llm_service()
    
    async def extract_insights(self, 
                              conversation_history: list) -> Optional[LeadInsight]:
        """Extract insights from conversation"""
        try:
            # Prepare conversation text
            conversation_text = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history
            ])
            
            messages = [
                {
                    "role": "user",
                    "content": f"""Extract lead intelligence from this conversation:

{conversation_text}

Respond ONLY with valid JSON."""
                }
            ]
            
            response = await self.llm_service.generate_response(
                messages=messages,
                system_prompt=LEAD_INTELLIGENCE_PROMPT,
                temperature=0.3,
                max_tokens=512
            )
            
            # Parse JSON response
            try:
                data = json.loads(response)
                insights = LeadInsight(
                    budget_min=data.get('budget_min'),
                    budget_max=data.get('budget_max'),
                    preferred_locations=data.get('preferred_locations', []),
                    property_types=[PropertyType(t) for t in data.get('property_types', [])],
                    urgency=data.get('urgency'),
                    objections=data.get('objections', []),
                    buying_intent_score=data.get('buying_intent_score', 0.5),
                    preferred_amenities=data.get('preferred_amenities', []),
                    family_size=data.get('family_size'),
                    move_timeline=data.get('move_timeline')
                )
                return insights
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing lead insights: {e}")
                return None
        
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            return None
