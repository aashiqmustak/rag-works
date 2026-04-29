"""
Call API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
import uuid

from models.schemas import VoiceCallRequest, VoiceCallResponse, CallStatus, CallSummary
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/calls", tags=["calls"])

# In-memory call storage
calls_db: dict = {}


@router.post("/initiate")
async def initiate_call(request: VoiceCallRequest) -> VoiceCallResponse:
    """Initiate outbound voice call"""
    try:
        call_id = str(uuid.uuid4())
        
        # TODO: Integrate with Pipecat voice pipeline
        
        calls_db[call_id] = {
            "call_id": call_id,
            "phone_number": request.phone_number,
            "lead_name": request.lead_name,
            "status": CallStatus.INITIATED,
            "created_at": datetime.now()
        }
        
        return VoiceCallResponse(
            call_id=call_id,
            status=CallStatus.INITIATED,
            lead_id="",  # Will be linked during call
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}")
async def get_call_status(call_id: str) -> dict:
    """Get call status"""
    try:
        if call_id not in calls_db:
            raise HTTPException(status_code=404, detail="Call not found")
        
        return calls_db[call_id]
    
    except Exception as e:
        logger.error(f"Error fetching call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{call_id}/end")
async def end_call(call_id: str, summary: Optional[dict] = None) -> dict:
    """End call and save summary"""
    try:
        if call_id not in calls_db:
            raise HTTPException(status_code=404, detail="Call not found")
        
        calls_db[call_id]["status"] = CallStatus.COMPLETED
        calls_db[call_id]["ended_at"] = datetime.now()
        calls_db[call_id]["summary"] = summary
        
        return {
            "status": "success",
            "call_id": call_id,
            "message": "Call ended"
        }
    
    except Exception as e:
        logger.error(f"Error ending call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_calls() -> dict:
    """List all calls"""
    try:
        return {
            "total": len(calls_db),
            "calls": list(calls_db.values())
        }
    
    except Exception as e:
        logger.error(f"Error listing calls: {e}")
        raise HTTPException(status_code=500, detail=str(e))
