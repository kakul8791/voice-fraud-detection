from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import time
import librosa

from analyzer import analyze_audio

app = FastAPI(title="AI Voice Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Body Schema (GUVI)
# -----------------------------
class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.get("/")
def root():
    return {"status": "AI Voice Fraud Detection API Running"}


@app.post("/detect")
async def detect_audio(req: AudioRequest):
    try:
        start = time.time()

        # Decode base64 audio
        audio_bytes = base64.b64decode(req.audio_base64)
        audio_buffer = io.BytesIO(audio_bytes)

        # Load audio
        y, sr = librosa.load(audio_buffer, sr=None, mono=True)

        # Analyze
        result = analyze_audio(y, sr)

        classification = (
            "AI_GENERATED" if result["ai_score"] >= 0.65 else "HUMAN"
        )

        return {
            "classification": classification,
            "confidence": round(result["ai_score"], 2),
            "explanation": result["flags"],
            "language": req.language,
            "audio_format": req.audio_format,
            "processing_time": round(time.time() - start, 2),
        }

    except Exception as e:
        return {
            "error": str(e)
        }
