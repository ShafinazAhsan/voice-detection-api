import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import time


# =========================
# Audio loading (SAFE)
# =========================
def load_audio_from_bytes(audio_bytes: bytes, target_sr: int = 16000):
    """
    Load audio bytes into mono waveform using librosa + soundfile
    (avoids torchaudio / ffmpeg issues on macOS)
    """
    with BytesIO(audio_bytes) as bio:
        audio, sr = sf.read(bio)

    # Convert stereo → mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Resample if needed
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr

    return audio, sr


# =========================
# Feature extraction
# =========================
def extract_features(audio: np.ndarray, sr: int):
    duration = librosa.get_duration(y=audio, sr=sr)

    # Silence ratio
    rms = librosa.feature.rms(y=audio)[0]
    silence_ratio = np.mean(rms < 0.01)

    # Spectral features
    centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sr))

    # Pitch variability
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    pitch_variance = np.var(pitch_values) if pitch_values.size > 0 else 0.0

    return {
        "duration": duration,
        "silence_ratio": silence_ratio,
        "centroid": centroid,
        "bandwidth": bandwidth,
        "pitch_variance": pitch_variance,
    }


# =========================
# Prediction logic (ML-style heuristic)
# =========================
def predict_voice(audio_bytes: bytes):
    start_time = time.time()

    audio, sr = load_audio_from_bytes(audio_bytes)
    features = extract_features(audio, sr)

    duration = features["duration"]
    silence_ratio = features["silence_ratio"]
    pitch_variance = features["pitch_variance"]

    # ---- Heuristic classifier (replace with ML later) ----
    if duration < 1.0:
        classification = "AI_GENERATED"
        confidence = 0.85
        explanation = "Very short duration typical of synthetic samples"

    elif pitch_variance < 50 and silence_ratio < 0.1:
        classification = "AI_GENERATED"
        confidence = 0.78
        explanation = "Low pitch variance and uniform energy suggest synthetic voice"

    else:
        classification = "HUMAN_GENERATED"
        confidence = 0.90
        explanation = "Natural pitch variation and pauses consistent with human speech"

    processing_time_ms = int((time.time() - start_time) * 1000)

    return {
        "classification": classification,
        "confidence": round(confidence, 2),
        "explanation": explanation,
        "processing_time_ms": processing_time_ms,
    }
