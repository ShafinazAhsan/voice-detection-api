from pydantic import BaseModel, Field
from typing import Optional


class VoiceRequest(BaseModel):
    language: str

    # GUVI Endpoint Tester sends this field
    audio_base64_format: Optional[str] = Field(
        default=None,
        alias="audio_base64_format"
    )

    # Direct API / evaluator support
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None


class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
