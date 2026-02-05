import requests
import librosa
import numpy as np
import tempfile
import os

def analyze_audio(audio_url: str):
    response = requests.get(audio_url, timeout=10)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        f.write(response.content)
        temp_path = f.name

    try:
        y, sr = librosa.load(temp_path, sr=None)

        duration = librosa.get_duration(y=y, sr=sr)
        energy = np.mean(y ** 2)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))

        ai_likelihood = 0.0
        if zcr < 0.04:
            ai_likelihood += 0.4
        if energy < 0.01:
            ai_likelihood += 0.3
        if duration > 8:
            ai_likelihood += 0.2

        ai_likelihood = min(ai_likelihood, 1.0)

        return {
            "duration_seconds": round(duration, 2),
            "energy": round(float(energy), 6),
            "zero_crossing_rate": round(float(zcr), 6),
            "ai_generated_probability": round(ai_likelihood, 2),
            "classification": "AI_GENERATED" if ai_likelihood >= 0.5 else "HUMAN"
        }

    finally:
        os.remove(temp_path)
