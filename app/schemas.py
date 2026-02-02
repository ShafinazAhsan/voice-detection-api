from pydantic import BaseModel, Field, model_validator
from typing import Optional


class VoiceRequest(BaseModel):
    audio_base64: Optional[str] = Field(
        None, description="Base64-encoded MP3 audio"
    )
    audio_url: Optional[str] = Field(
        None, description="Public URL to MP3 audio file"
    )
    language: str = Field(..., example="en")
    message: Optional[str] = Field(
        None, description="Optional test description"
    )

    @model_validator(mode="after")
    def validate_audio_input(self):
        if not self.audio_base64 and not self.audio_url:
            raise ValueError("Either audio_base64 or audio_url must be provided")
        return self


class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str
    processing_time_ms: int
