"""
Voice pipeline initialization in FastAPI
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

from voice.pipeline import get_voice_pipeline
from models.schemas import VoiceCallRequest, VoiceCallResponse, CallStatus
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/voice", tags=["voice"])

voice_pipeline = get_voice_pipeline()


@router.post("/initiate-call")
async def initiate_call(request: VoiceCallRequest) -> VoiceCallResponse:
    """Initiate outbound voice call"""
    try:
        call_id = await voice_pipeline.start_outbound_call(
            phone_number=request.phone_number,
            lead_name=request.lead_name,
            initial_prompt=request.script
        )
        
        if not call_id:
            raise HTTPException(status_code=500, detail="Failed to initiate call")
        
        return VoiceCallResponse(
            call_id=call_id,
            status=CallStatus.INITIATED,
            lead_id="",
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/handle-inbound")
async def handle_inbound(phone_number: str) -> dict:
    """Handle inbound call"""
    try:
        call_id = str(uuid.uuid4())
        
        success = await voice_pipeline.handle_inbound_call(
            call_id=call_id,
            from_number=phone_number
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to handle inbound call")
        
        return {
            "call_id": call_id,
            "status": "connected"
        }
    
    except Exception as e:
        logger.error(f"Error handling inbound call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{call_id}/stream")
async def stream_audio(call_id: str, audio_data: bytes) -> dict:
    """Stream audio to call"""
    try:
        success = await voice_pipeline.stream_audio(call_id, audio_data)
        
        return {
            "status": "success" if success else "failed",
            "call_id": call_id
        }
    
    except Exception as e:
        logger.error(f"Error streaming audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}/transcription")
async def get_transcription(call_id: str) -> dict:
    """Get call transcription"""
    try:
        transcription = await voice_pipeline.transcribe_call(call_id)
        
        return {
            "call_id": call_id,
            "transcription": transcription or ""
        }
    
    except Exception as e:
        logger.error(f"Error getting transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{call_id}/end")
async def end_call(call_id: str, reason: str = "completed") -> dict:
    """End call"""
    try:
        success = await voice_pipeline.end_call(call_id, reason)
        
        if not success:
            raise HTTPException(status_code=404, detail="Call not found")
        
        call_info = voice_pipeline.get_call_info(call_id)
        
        return {
            "status": "ended",
            "call_id": call_id,
            "duration_seconds": call_info.get("duration_seconds", 0),
            "reason": reason
        }
    
    except Exception as e:
        logger.error(f"Error ending call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{call_id}")
async def get_call_status(call_id: str) -> dict:
    """Get call status"""
    try:
        call_info = voice_pipeline.get_call_info(call_id)
        
        if not call_info:
            raise HTTPException(status_code=404, detail="Call not found")
        
        return call_info
    
    except Exception as e:
        logger.error(f"Error getting call status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active-calls")
async def get_active_calls() -> dict:
    """Get all active calls"""
    try:
        calls = voice_pipeline.get_active_calls()
        
        return {
            "total": len(calls),
            "calls": calls
        }
    
    except Exception as e:
        logger.error(f"Error getting active calls: {e}")
        raise HTTPException(status_code=500, detail=str(e))
