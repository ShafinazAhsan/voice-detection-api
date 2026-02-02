import base64
import io
import requests
from fastapi import HTTPException


def decode_base64_audio(audio_base64: str) -> bytes:
    """
    Decode base64-encoded audio (MP3/WAV) into raw bytes
    """
    try:
        return base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Invalid base64 audio data"
        )


def download_audio_from_url(audio_url: str) -> bytes:
    """
    Download audio file from a public URL and return bytes
    """
    try:
        response = requests.get(audio_url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Failed to download audio from URL"
        )
