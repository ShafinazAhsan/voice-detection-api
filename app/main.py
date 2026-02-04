# app/main.py
from fastapi import FastAPI, Header, HTTPException, Form
from app.auth import verify_api_key
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice
from app.schemas import DetectVoiceResponse
import time

app = FastAPI()


@app.post("/detect-voice", response_model=DetectVoiceResponse)
def detect_voice(
    x_api_key: str = Header(..., alias="x-api-key"),
    language: str = Form(...),
    audio_format: str = Form(...),
    audio_base64: str | None = Form(None),
    audio_url: str | None = Form(None),
):
    verify_api_key(x_api_key)

    if not audio_base64 and not audio_url:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided"
        )

    start = time.time()

    if audio_base64:
        audio_bytes = decode_base64_audio(audio_base64)
    else:
        audio_bytes = download_audio_from_url(audio_url)

    result = predict_voice(audio_bytes)

    return DetectVoiceResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        language=language,
        explanation=result["explanation"],
        processing_time_ms=int((time.time() - start) * 1000)
    )
