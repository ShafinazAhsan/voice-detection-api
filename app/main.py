import time
from fastapi import FastAPI, Depends, HTTPException

from app.schemas import VoiceDetectionRequest, VoiceDetectionResponse
from app.auth import verify_api_key
from app.audio_utils import decode_base64_audio
from app.inference import predict_voice

app = FastAPI(title="AI Voice Detection API")


@app.post("/detect-voice", response_model=VoiceDetectionResponse)
def detect_voice(
    request: VoiceDetectionRequest,
    _: str = Depends(verify_api_key)
):
    start_time = time.time()

    # Validate language
    if request.language not in ["ta", "en", "hi", "ml", "te"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Validate audio
    try:
        _ = decode_base64_audio(request.audio_base64)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Mock inference
    result = predict_voice(request.language)

    processing_time = int((time.time() - start_time) * 1000)

    return {
        **result,
        "processing_time_ms": processing_time
    }
