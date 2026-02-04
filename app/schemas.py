from pydantic import BaseModel, Field
from typing import Optional


class VoiceRequest(BaseModel):
    language: str = Field(..., example="en")

    # Standard API field
    audio_base64: Optional[str] = Field(
        None, description="Base64-encoded audio"
    )

    # GUVI-specific field (VERY IMPORTANT)
    audio_base64_format: Optional[str] = Field(
        None, description="Base64-encoded audio (GUVI tester)"
    )

    # Optional URL input
    audio_url: Optional[str] = None


class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
