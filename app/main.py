from fastapi import FastAPI, Depends, HTTPException, Request
import time

from app.auth import verify_api_key
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice

app = FastAPI(
    title="AI Voice Detection API",
    version="1.0.0",
)

SUPPORTED_LANGUAGES = {"en", "ta", "hi", "ml", "te"}


@app.post("/detect-voice")
async def detect_voice(
    request: Request,
    _: None = Depends(verify_api_key)
):
    start_time = time.time()

    # --- Read JSON or FORM ---
    content_type = request.headers.get("content-type", "")

    data = {}
    if "application/json" in content_type:
        data = await request.json()
    else:
        form = await request.form()
        data = dict(form)

    language = data.get("language")
    if not language:
        raise HTTPException(status_code=422, detail="language is required")

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {SUPPORTED_LANGUAGES}"
        )

    # 🔑 Accept ALL possible audio fields
    audio_base64 = (
        data.get("audio_base64")
        or data.get("audio_base64_format")
    )

    audio_url = data.get("audio_url")

    if audio_base64:
        audio_bytes = decode_base64_audio(audio_base64)
    elif audio_url:
        audio_bytes = download_audio_from_url(audio_url)
    else:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided"
        )

    result = predict_voice(audio_bytes)

    processing_time_ms = int((time.time() - start_time) * 1000)

    return {
        "classification": result["classification"],
        "confidence": result["confidence"],
        "language": language,
        "explanation": result["explanation"],
        "processing_time_ms": processing_time_ms,
    }
