import os
import io
import pandas as pd
from huggingface_hub import hf_hub_download
from tqdm import tqdm
from pydub import AudioSegment

# Configuration
INDIC_LANGS = {
    'hindi': {
        'human': ('google/fleurs', 'hi_in/train/0000.parquet', 'refs/convert/parquet'),
        'ai': ('vdivyasharma/IndicSynth', 'Hindi/train-00000-of-00107.parquet', 'main')
    },
    'tamil': {
        'human': ('google/fleurs', 'ta_in/train/0000.parquet', 'refs/convert/parquet'),
        'ai': ('vdivyasharma/IndicSynth', 'Tamil/train-00000-of-00171.parquet', 'main')
    },
    'telugu': {
        'human': ('google/fleurs', 'te_in/train/0000.parquet', 'refs/convert/parquet'),
        'ai': ('vdivyasharma/IndicSynth', 'Telugu/train-00000-of-00129.parquet', 'main')
    },
    'malayalam': {
        'human': ('google/fleurs', 'ml_in/train/0000.parquet', 'refs/convert/parquet'),
        'ai': ('vdivyasharma/IndicSynth', 'Malayalam/train-00000-of-00032.parquet', 'main')
    }
}

SAMPLES_PER_CLASS = 150 # 150 Real, 150 AI per language
OUTPUT_DIR = 'indic_data'

# Initialize static-ffmpeg for pydub support
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

def download_and_save_samples():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for lang, configs in INDIC_LANGS.items():
        print(f"\n--- Processing {lang.upper()} ---")
        lang_dir = os.path.join(OUTPUT_DIR, lang)
        
        for category in ['human', 'ai']:
            cat_dir = os.path.join(lang_dir, category)
            os.makedirs(cat_dir, exist_ok=True)
            
            repo, filename, revision = configs[category]
            print(f"Downloading {category} Parquet from {repo}...")
            
            try:
                parquet_file = hf_hub_download(
                    repo_id=repo,
                    filename=filename,
                    repo_type='dataset',
                    revision=revision
                )
                
                df = pd.read_parquet(parquet_file)
                # Take first N samples
                subset = df.head(SAMPLES_PER_CLASS)
                
                for i, row in tqdm(subset.iterrows(), total=len(subset), desc=f"Saving {category}"):
                    audio_entry = row['audio']
                    audio_bytes = audio_entry['bytes']
                    
                    # Convert to WAV using pydub
                    with io.BytesIO(audio_bytes) as bio:
                        segment = AudioSegment.from_file(bio)
                        # We save as wav to make loading fast during training
                        output_path = os.path.join(cat_dir, f"{category}_{i}.wav")
                        segment.export(output_path, format="wav")
                        
            except Exception as e:
                print(f"Error processing {lang} {category}: {e}")

if __name__ == "__main__":
    download_and_save_samples()
    print("\nMulti-lingual dataset (Parquet-based) download complete!")
