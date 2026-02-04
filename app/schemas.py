from pydantic import BaseModel, Field
from typing import Optional


class VoiceDetectRequest(BaseModel):
    language: str = Field(..., example="en")

    # Standard API inputs
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None

    # GUVI-specific fields
    audio_format: Optional[str] = None
    audio_base64_format: Optional[str] = None


class VoiceDetectResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
