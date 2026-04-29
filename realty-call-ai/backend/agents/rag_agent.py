"""
RAG Agent for property retrieval
"""
from typing import List, Dict, Optional
from models.schemas import PropertyListing
from rag.pipeline import get_rag_pipeline
from services.llm_service import get_llm_service
from prompts.agent_prompts import RAG_AGENT_PROMPT
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RAGAgent:
    """RAG Agent for property retrieval"""
    
    def __init__(self):
        """Initialize agent"""
        self.rag_pipeline = get_rag_pipeline()
        self.llm_service = get_llm_service()
    
    async def search_properties(self, 
                               query: str,
                               filters: Optional[Dict] = None,
                               top_k: int = 5) -> List[PropertyListing]:
        """Search for properties"""
        try:
            if filters:
                # Use filter-based search
                results = self.rag_pipeline.search_by_filters(filters)
                return results[:top_k]
            else:
                # Use semantic search
                results, scores = self.rag_pipeline.search(query, top_k)
                return results
        
        except Exception as e:
            logger.error(f"Error searching properties: {e}")
            return []
    
    async def format_property_response(self, 
                                      properties: List[PropertyListing],
                                      user_query: str) -> str:
        """Format property list for display"""
        try:
            if not properties:
                return "I couldn't find properties matching your criteria. Could you tell me more about what you're looking for?"
            
            props_text = "\n".join([
                f"• {p.title} - {p.location} - ${p.price:,.0f} "
                f"({p.bedrooms}BR/{p.bathrooms}BA, {p.area_sqft}sqft)"
                for p in properties
            ])
            
            messages = [
                {
                    "role": "user",
                    "content": f"""Format these property recommendations nicely:

User query: {user_query}

Properties:
{props_text}

Provide a friendly, conversational response highlighting the best matches."""
                }
            ]
            
            response = await self.llm_service.generate_response(
                messages=messages,
                system_prompt=RAG_AGENT_PROMPT,
                temperature=0.7,
                max_tokens=512
            )
            
            return response
        
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "I found some properties but couldn't format them properly."
