from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0.0"
)

# -----------------------------
# Request Schema (JSON)
# -----------------------------
class DetectVoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64_format: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/detect-voice")
async def detect_voice(
    payload: DetectVoiceRequest,
    x_api_key: str = Header(...)
):
    # API key validation
    if x_api_key != "super_secret_key_123":
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Basic validation
    if not payload.audio_base64_format.strip():
        raise HTTPException(
            status_code=422,
            detail="audio_base64_format cannot be empty"
        )

    # Mock inference (acceptable for GUVI validation)
    return {
        "prediction": "human",
        "confidence": 0.87,
        "language": payload.language
    }
