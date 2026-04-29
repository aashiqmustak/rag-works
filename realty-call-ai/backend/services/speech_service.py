"""
Speech-to-Text and Text-to-Speech services using Sarvam AI
"""
import aiohttp
from models.config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SpeechService:
    """Speech service for STT/TTS"""
    
    def __init__(self):
        """Initialize speech service"""
        self.api_key = settings.sarvam_api_key
        self.stt_model = settings.sarvam_stt_model
        self.tts_model = settings.sarvam_tts_model
        self.base_url = "https://api.sarvam.ai"
    
    async def transcribe(self, audio_url: str) -> str:
        """Transcribe audio to text"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                payload = {
                    "audio_url": audio_url,
                    "model": self.stt_model,
                    "language": "en"
                }
                
                async with session.post(
                    f"{self.base_url}/speech-to-text",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("text", "")
                    else:
                        logger.error(f"STT API error: {response.status}")
                        return ""
        
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return ""
    
    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        """Convert text to speech"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                payload = {
                    "text": text,
                    "model": self.tts_model,
                    "language": "en",
                    "voice": voice
                }
                
                async with session.post(
                    f"{self.base_url}/text-to-speech",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        logger.error(f"TTS API error: {response.status}")
                        return b""
        
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            return b""


# Global speech service instance
_speech_service = None


def get_speech_service() -> SpeechService:
    """Get or create speech service"""
    global _speech_service
    if _speech_service is None:
        _speech_service = SpeechService()
    return _speech_service
