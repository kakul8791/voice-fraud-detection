import numpy as np
import librosa


def analyze_audio(y, sr):
    rms = float(np.mean(librosa.feature.rms(y=y)))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

    confidence = 0.0
    flags = []

    if flatness > 0.60:
        confidence += 0.4
        flags.append("high spectral flatness (synthetic smoothness)")

    if zcr < 0.025:
        confidence += 0.35
        flags.append("low pitch variance")

    if rms < 0.010:
        confidence += 0.15
        flags.append("over-clean signal")

    return {
        "ai_score": min(confidence, 1.0),
        "flags": flags,
        "features": {
            "rms": rms,
            "zcr": zcr,
            "spectral_centroid": centroid,
            "spectral_flatness": flatness
        }
    }
