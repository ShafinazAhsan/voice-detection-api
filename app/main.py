from fastapi import FastAPI, Depends, HTTPException
from time import time

from app.schemas import VoiceRequest, VoiceResponse
from app.auth import verify_api_key
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0"
)


@app.post("/detect-voice", response_model=VoiceResponse)
def detect_voice(
    request: VoiceRequest,
    _: str = Depends(verify_api_key)
):
    start_time = time()

    # ---- AUDIO INPUT HANDLING (GUVI + Evaluators) ----
    if request.audio_base64:
        audio_bytes = decode_base64_audio(request.audio_base64)

    elif request.audio_base64_format:
        audio_bytes = decode_base64_audio(request.audio_base64_format)

    elif request.audio_url:
        audio_bytes = download_audio_from_url(request.audio_url)

    else:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided"
        )

    # ---- ML INFERENCE ----
    result = predict_voice(audio_bytes)

    processing_time_ms = int((time() - start_time) * 1000)

    return VoiceResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        language=request.language,
        explanation=result["explanation"],
        processing_time_ms=processing_time_ms
    )
