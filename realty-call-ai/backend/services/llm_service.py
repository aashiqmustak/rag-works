"""
LLM service for Groq API integration
"""
from groq import Groq
from models.config import settings
from utils.logger import setup_logger
from typing import Optional

logger = setup_logger(__name__)


class LLMService:
    """LLM service using Groq API"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "mixtral-8x7b-32768"  # Default Groq model
    
    async def generate_response(self, 
                               messages: list,
                               temperature: float = 0.7,
                               max_tokens: int = 1024,
                               system_prompt: Optional[str] = None) -> str:
        """Generate response from LLM"""
        try:
            # Prepare messages
            prepared_messages = []
            
            if system_prompt:
                prepared_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            prepared_messages.extend(messages)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prepared_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def stream_response(self, 
                             messages: list,
                             temperature: float = 0.7,
                             max_tokens: int = 1024,
                             system_prompt: Optional[str] = None):
        """Stream response from LLM"""
        try:
            prepared_messages = []
            
            if system_prompt:
                prepared_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            prepared_messages.extend(messages)
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=prepared_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise


# Global LLM instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create LLM service"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
