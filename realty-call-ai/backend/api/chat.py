"""
Chat API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime

from models.schemas import (
    ChatRequest, ChatResponse, ChatMessage, 
    ConversationContext, LeadInsight
)
from agents.supervisor_agent import SupervisorAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory storage (use database in production)
conversations: dict = {}
supervisor = SupervisorAgent()


@router.post("/send")
async def send_message(request: ChatRequest) -> ChatResponse:
    """Send a chat message"""
    try:
        # Initialize conversation if needed
        if request.lead_id not in conversations:
            conversations[request.lead_id] = {
                "history": [],
                "lead_id": request.lead_id,
                "insights": None
            }
        
        conv = conversations[request.lead_id]
        
        # Add user message
        user_msg = ChatMessage(
            id=str(uuid.uuid4()),
            lead_id=request.lead_id,
            role="user",
            content=request.content,
            timestamp=datetime.now()
        )
        conv["history"].append(user_msg)
        
        # Build context
        context = ConversationContext(
            lead_id=request.lead_id,
            conversation_history=conv["history"],
            current_lead_insights=conv["insights"] or LeadInsight()
        )
        
        # Process message through supervisor
        result = await supervisor.process_message(request.content, context)
        
        # Add assistant message
        assistant_msg = ChatMessage(
            id=str(uuid.uuid4()),
            lead_id=request.lead_id,
            role="assistant",
            content=result["response"],
            timestamp=datetime.now()
        )
        conv["history"].append(assistant_msg)
        conv["insights"] = result["insights"]
        
        # Build response
        return ChatResponse(
            response=result["response"],
            properties_recommended=result["properties"],
            lead_insights=result["insights"],
            action_items=result["action_items"]
        )
    
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{lead_id}")
async def get_chat_history(lead_id: str) -> dict:
    """Get chat history for a lead"""
    try:
        if lead_id not in conversations:
            return {"history": [], "lead_id": lead_id}
        
        conv = conversations[lead_id]
        return {
            "history": conv["history"],
            "lead_id": lead_id,
            "insights": conv["insights"]
        }
    
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{lead_id}")
async def clear_history(lead_id: str) -> dict:
    """Clear chat history"""
    try:
        if lead_id in conversations:
            del conversations[lead_id]
        
        return {"status": "cleared", "lead_id": lead_id}
    
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
