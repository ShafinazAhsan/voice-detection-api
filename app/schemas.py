# app/schemas.py
from pydantic import BaseModel
from typing import Optional


class DetectVoiceResponse(BaseModel):
    classification: str
    confidence: float
    explanation: str
    processing_time_ms: int
