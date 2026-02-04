from fastapi import FastAPI, Depends, HTTPException
from app.schemas import VoiceDetectRequest, VoiceDetectResponse
from app.auth import verify_api_key
from app.audio_utils import decode_base64_audio, download_audio_from_url
from app.inference import predict_voice
import time

app = FastAPI(title="AI Generated Voice Detection API")


@app.post("/detect-voice", response_model=VoiceDetectResponse)
def detect_voice(
    request: VoiceDetectRequest,
    api_key: str = Depends(verify_api_key),
):
    start_time = time.time()

    # ✅ Normalize GUVI → internal format
    audio_bytes = None

    if request.audio_base64:
        audio_bytes = decode_base64_audio(request.audio_base64)

    elif request.audio_base64_format:
        audio_bytes = decode_base64_audio(request.audio_base64_format)

    elif request.audio_url:
        audio_bytes = download_audio_from_url(request.audio_url)

    else:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided",
        )

    result = predict_voice(audio_bytes)

    return VoiceDetectResponse(
        classification=result["classification"],
        confidence=result["confidence"],
        language=request.language,
        explanation=result["explanation"],
        processing_time_ms=int((time.time() - start_time) * 1000),
    )
