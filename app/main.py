from fastapi import FastAPI, Form, Header, HTTPException

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/detect-voice")
async def detect_voice(
    language: str = Form(...),
    audio_format: str = Form(...),
    audio_base64_format: str = Form(...),
    x_api_key: str = Header(...)
):
    # API key validation
    if x_api_key != "super_secret_key_123":
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Validate required fields
    if not language:
        raise HTTPException(status_code=422, detail="Language is required")

    if not audio_format:
        raise HTTPException(status_code=422, detail="Audio format is required")

    if not audio_base64_format:
        raise HTTPException(
            status_code=422,
            detail="Either audio_base64 or audio_url must be provided"
        )

    # (Mock inference – allowed for hackathon validation)
    return {
        "prediction": "human",
        "confidence": 0.87
    }
