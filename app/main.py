from fastapi import FastAPI, Depends, HTTPException, Header
from dotenv import load_dotenv
import os
import time

from app.auth import verify_api_key
from app.schemas import DetectVoiceResponse
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice
from pydantic import BaseModel, Field

# Load .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
load_dotenv()

app = FastAPI(
    title="AI Voice Detection API",
    version="1.0.0",
    description="Detect whether a voice sample is AI-generated or human-generated"
)

# Request schema (GUVI-compatible)
class DetectVoiceRequest(BaseModel):
    language: str = "en"
    audio_format: str = Field("mp3", alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        populate_by_name = True

@app.get("/")
def health():
    return {"status": "ok"}

@app.post(
    "/detect-voice",
    response_model=DetectVoiceResponse,
    summary="Detect Voice",
    description="Classifies an audio sample as AI-generated or human-generated"
)
async def detect_voice(
    payload: DetectVoiceRequest,
    x_api_key: str = Header(..., alias="x-api-key")
):
    start_time = time.time()

    # 🔹 API Key Validation (uses the env-based key we set up)
    if not verify_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not payload.audio_base64.strip():
        raise HTTPException(
            status_code=422,
            detail="audioBase64 cannot be empty"
        )

    # 🔹 Audio input handling
    try:
        audio_bytes = decode_base64_audio(payload.audio_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid audio encoding: {str(e)}")

    # 🔹 ML inference
    result = predict_voice(audio_bytes)
    processing_time_ms = int((time.time() - start_time) * 1000)

    return DetectVoiceResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        explanation=result["explanation"],
        processing_time_ms=processing_time_ms
    )
