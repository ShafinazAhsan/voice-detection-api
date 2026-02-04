import numpy as np
import librosa
import time
import joblib
import os
from pydub import AudioSegment
import io

# --- Added for Windows MP3/M4A Support ---
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass
# -----------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "voice_model.joblib")

try:
    voice_model = joblib.load(MODEL_PATH)
    print(f"Voice Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    voice_model = None
    print(f"Warning: Could not load voice model: {e}")


# =========================
# Audio loading (SAFE)
# =========================
def load_audio_from_bytes(audio_bytes: bytes, target_sr: int = 16000):
    """
    Load audio bytes using pydub (handles MP3/M4A/etc) and convert to librosa format
    """
    with io.BytesIO(audio_bytes) as bio:
        # pydub can read from any byte stream if ffmpeg is in path
        audio_segment = AudioSegment.from_file(bio)
        
        # Standardize for ML
        audio_segment = audio_segment.set_frame_rate(target_sr).set_channels(1)
        
        # Convert to numpy array (librosa format)
        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        
        # Normalize to [-1.0, 1.0]
        max_val = float(1 << (8 * audio_segment.sample_width - 1))
        samples /= max_val
        
        return samples, target_sr


# =========================
# Feature extraction (Aligns with training)
# =========================
def extract_comprehensive_features(audio, sr):
    # 1. MFCCs (40 instead of 20)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    mfccs_std = np.std(mfccs.T, axis=0)
    
    # 2. Spectral Features
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sr).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sr).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr).T, axis=0)
    
    return np.hstack([mfccs_mean, mfccs_std, chroma, mel, contrast, tonnetz])


# =========================
# Prediction logic (ML Model)
# =========================
def predict_voice(audio_bytes: bytes):
    start_time = time.time()

    try:
        audio, sr = load_audio_from_bytes(audio_bytes)
        
        if voice_model is not None:
            # 🔹 ML Prediction
            features = extract_comprehensive_features(audio, sr)
            features = features.reshape(1, -1)
            
            # --- Detect Voice (Human vs AI) ---
            prediction = voice_model.predict(features)[0]
            probabilities = voice_model.predict_proba(features)[0]
            
            if prediction == 1:
                classification = "AI_GENERATED"
                confidence = float(probabilities[1])
                explanation = "Acoustic fingerprints match patterns typically found in synthetic voice models."
            else:
                classification = "HUMAN_GENERATED"
                confidence = float(probabilities[0])
                explanation = "Spectral variance and harmonic structure are consistent with natural human speech."
        
        else:
            # 🔹 Fallback Heuristic logic (if model fails to load)
            rms = librosa.feature.rms(y=audio)[0]
            silence_ratio = np.mean(rms < 0.01)
            
            if silence_ratio < 0.05:
                classification = "AI_GENERATED"
                confidence = 0.51
                explanation = "Unusually low silence patterns detected (fallback)."
            else:
                classification = "HUMAN_GENERATED"
                confidence = 0.51
                explanation = "Natural silence patterns detected (fallback)."

    except Exception as e:
        return {
            "classification": "ERROR",
            "confidence": 0.0,
            "explanation": f"Inference failed: {str(e)}",
            "processing_time_ms": int((time.time() - start_time) * 1000),
        }

    processing_time_ms = int((time.time() - start_time) * 1000)
    return {
        "classification": classification,
        "confidence": round(float(confidence), 2),
        "explanation": explanation,
        "processing_time_ms": processing_time_ms
    }
