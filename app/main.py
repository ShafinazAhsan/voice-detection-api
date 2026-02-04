from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
import os
import time

from app.auth import verify_api_key
from app.schemas import VoiceRequest, VoiceResponse
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice

# Load .env from app directory if it exists, otherwise fallback to root
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)
load_dotenv()

app = FastAPI(
    title="AI Voice Detection API",
    version="1.0.0",
    description="Detect whether a voice sample is AI-generated or human-generated"
)

SUPPORTED_LANGUAGES = {"en", "ta", "hi", "ml", "te"}

@app.post(
    "/detect-voice",
    response_model=VoiceResponse,
    summary="Detect Voice",
    description="Classifies an audio sample as AI-generated or human-generated"
)
def detect_voice(
    request: VoiceRequest,
    _: None = Depends(verify_api_key)
):
    start_time = time.time()

    # 🔹 Language validation
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {sorted(SUPPORTED_LANGUAGES)}"
        )

    # 🔹 Audio input handling (Base64 OR URL)
    if request.audio_base64:
        audio_bytes = decode_base64_audio(request.audio_base64)

    elif request.audio_url:
        audio_bytes = download_audio_from_url(request.audio_url)

    else:
        raise HTTPException(
            status_code=400,
            detail="Audio input missing (provide audio_base64 or audio_url)"
        )

    # 🔹 ML inference (currently mock / placeholder)
    result = predict_voice(audio_bytes)

    processing_time_ms = int((time.time() - start_time) * 1000)

    return VoiceResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        explanation=result["explanation"],
        processing_time_ms=processing_time_ms
    )
