from pydantic import BaseModel, Field
from typing import Optional

class VoiceDetectionRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded MP3 audio")
    language: str = Field(..., description="ta | en | hi | ml | te")
    message: Optional[str] = None


class VoiceDetectionResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
