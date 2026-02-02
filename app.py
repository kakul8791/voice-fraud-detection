from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import librosa
import soundfile as sf
import io
import time

from analyzer import analyze_audio

app = FastAPI(title="AI Voice Fraud Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI Voice Fraud Detection API Running"}

@app.post("/detect")
async def detect_audio(file: UploadFile = File(...)):
    start = time.time()

    try:
        audio_bytes = await file.read()
        audio_buffer = io.BytesIO(audio_bytes)

        y, sr = librosa.load(audio_buffer, sr=None, mono=True)

        result = analyze_audio(y, sr)

        classification = "AI_GENERATED" if ai_score >= 0.5 else "HUMAN"


        return {
            "success": True,
            "classification": classification,
            "confidence": round(result["ai_score"], 2),
            "explanation": result["flags"],
            "features": result["features"],
            "time_taken": round(time.time() - start, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
