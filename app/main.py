from fastapi import FastAPI, Depends, HTTPException
import time

from app.auth import verify_api_key
from app.schemas import VoiceRequest, VoiceResponse
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice

app = FastAPI(
    title="AI Voice Detection API",
    version="1.0.0",
)

SUPPORTED_LANGUAGES = {"en", "ta", "hi", "ml", "te"}


@app.post("/detect-voice", response_model=VoiceResponse)
def detect_voice(
    request: VoiceRequest,
    _: None = Depends(verify_api_key)
):
    start_time = time.time()

    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {SUPPORTED_LANGUAGES}"
        )

    # 🔑 GUVI + Standard compatibility logic
    audio_base64 = (
        request.audio_base64
        or request.audio_base64_format
    )

    if audio_base64:
        audio_bytes = decode_base64_audio(audio_base64)
    elif request.audio_url:
        audio_bytes = download_audio_from_url(request.audio_url)
    else:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided"
        )

    result = predict_voice(audio_bytes)

    processing_time_ms = int((time.time() - start_time) * 1000)

    return VoiceResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        language=request.language,
        explanation=result["explanation"],
        processing_time_ms=processing_time_ms,
    )
