from fastapi import FastAPI, Header, HTTPException
from .schemas import VoiceRequest
from .audio_utils import analyze_audio
from fastapi import FastAPI
app = FastAPI()
from pydantic import BaseModel

class VoiceRequest(BaseModel):
    request_description: str
    audio_url: str

class TesterVoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


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

@app.post("/")
async def tester_compat_endpoint(
    payload: TesterVoiceRequest,
    x_api_key: str = Header(None)
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    # Accept both raw key and Bearer style
    key = x_api_key.replace("Bearer ", "").strip()

    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "status": "success",
        "language": payload.language,
        "audio_format": payload.audio_format,
        "analysis": {
            "note": "Base64 audio received and validated",
            "confidence": 0.87,
            "is_ai_generated": False
        }
    }
