from fastapi import FastAPI, Header, HTTPException
from .schemas import VoiceRequest
from .audio_utils import analyze_audio

app = FastAPI()

API_KEY = "my-secret-key-123"

def verify_api_key(auth: str):
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API key")
    if auth.split(" ")[1] != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/api/voice-detection")
def detect_voice(req: VoiceRequest, authorization: str = Header(None)):
    verify_api_key(authorization)

    try:
        analysis = analyze_audio(req.audio_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "success",
        "request_description": req.request_description,
        "audio_analysis": analysis
    }
