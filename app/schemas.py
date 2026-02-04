from pydantic import BaseModel, Field
from typing import Optional


class VoiceDetectRequest(BaseModel):
    language: str

    # GUVI sends this
    audio_base64_format: Optional[str] = Field(
        default=None,
        description="Base64 encoded audio (GUVI field)"
    )

    # Evaluator / standard API sends this
    audio_base64: Optional[str] = Field(
        default=None,
        description="Base64 encoded audio"
    )

    audio_url: Optional[str] = None
    audio_format: Optional[str] = "mp3"


class VoiceDetectResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
