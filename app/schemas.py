from pydantic import BaseModel, Field
from typing import Optional

class VoiceDetectRequest(BaseModel):
    language: str = Field(..., example="en")

    # GUVI sends this
    audio_base64_format: Optional[str] = None

    # Standard API users may send this
    audio_base64: Optional[str] = None

    # Optional URL support
    audio_url: Optional[str] = None


class VoiceDetectResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
