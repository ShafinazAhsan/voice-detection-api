import base64

def decode_base64_audio(audio_base64: str) -> bytes:
    try:
        return base64.b64decode(audio_base64)
    except Exception:
        raise ValueError("Invalid base64 audio data")
