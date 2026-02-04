import os
import numpy as np
import librosa
from pydub import AudioSegment
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm import tqdm
from joblib import Parallel, delayed

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

def load_audio(file_path, target_sr=16000):
    try:
        audio_segment = AudioSegment.from_file(file_path)
        audio_segment = audio_segment.set_frame_rate(target_sr).set_channels(1)
        samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
        max_val = float(1 << (8 * audio_segment.sample_width - 1))
        samples /= max_val
        return samples, target_sr
    except:
        try:
            audio, sr = librosa.load(file_path, sr=target_sr)
            return audio, sr
        except:
            return None, None

def extract_features_single(item):
    file_path, v_lab, l_lab = item
    audio, sr = load_audio(file_path)
    if audio is None: return None
    
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    mfccs_std = np.std(mfccs.T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sr).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sr).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr).T, axis=0)
    
    feat = np.hstack([mfccs_mean, mfccs_std, chroma, mel, contrast, tonnetz])
    return feat, v_lab, l_lab

if __name__ == "__main__":
    data_sources = ['UK', 'USA', 'indic_data']
    all_raw_data = []
    for root in data_sources:
        if not os.path.exists(root): continue
        for subdir, dirs, files in os.walk(root):
            for file in files:
                if file.endswith(('.m4a', '.mp3', '.wav')):
                    fp = os.path.join(subdir, file)
                    pl = fp.lower().replace('\\', '/')
                    vl = 0 if ('original' in pl or '/human/' in pl) else 1
                    ll = 'en'
                    if '/hindi/' in pl: ll = 'hi'
                    elif '/tamil/' in pl: ll = 'ta'
                    elif '/telugu/' in pl: ll = 'te'
                    elif '/malayalam/' in pl: ll = 'ml'
                    all_raw_data.append((fp, vl, ll))
    
    print(f"Extracting features for {len(all_raw_data)} files using Parallel...")
    # Using 'threading' to avoid pickling issues with pydub on Windows
    results = Parallel(n_jobs=-1, backend="threading")(
        delayed(extract_features_single)(item) for item in tqdm(all_raw_data)
    )
    
    features, voice_y, lang_y = [], [], []
    for res in results:
        if res:
            features.append(res[0]); voice_y.append(res[1]); lang_y.append(res[2])
            
    X = np.array(features)
    
    # Train Models
    for name, targets, filename in [("Voice", voice_y, 'app/voice_model.joblib'), ("Language", lang_y, 'app/language_model.joblib')]:
        X_train, X_test, y_train, y_test = train_test_split(X, targets, test_size=0.15, stratify=targets)
        model = RandomForestClassifier(n_estimators=300, class_weight='balanced')
        model.fit(X_train, y_train)
        print(f"{name} Accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")
        joblib.dump(model, filename)
        if name == "Language": print(f"Languages: {model.classes_}")
