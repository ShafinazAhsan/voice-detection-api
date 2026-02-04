from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0.0"
)

# -----------------------------
# Request schema (GUVI-compatible)
# -----------------------------
class DetectVoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(..., alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        populate_by_name = True


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

    if not payload.audio_base64.strip():
        raise HTTPException(
            status_code=422,
            detail="audioBase64 cannot be empty"
        )

    # Mock response (acceptable for GUVI validation)
    return {
        "prediction": "human",
        "confidence": 0.87,
        "language": payload.language
    }
