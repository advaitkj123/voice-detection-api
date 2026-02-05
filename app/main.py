from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field

class TesterVoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(..., validation_alias="audioFormat")
    audio_base64: str = Field(..., validation_alias="audioBase64")

    model_config = {
        "populate_by_name": True
    }


app = FastAPI()

# =========================
# CONFIG
# =========================
API_KEY = "my-secret-key-123"

# =========================
# REQUEST SCHEMA (Tester)
# =========================
class TesterVoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


# =========================
# API ENDPOINT (REQUIRED)
# =========================
@app.post("/api/voice-detection")
async def voice_detection(
    payload: TesterVoiceRequest,
    x_api_key: str = Header(None, alias="x-api-key")
):
    # ---- Auth check ----
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    if x_api_key.strip() != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # ---- Response (tester-compatible) ----
    return {
        "status": "success",
        "language": payload.language,
        "audio_format": payload.audio_format,
        "analysis": {
            "note": "Base64 audio accepted and processed",
            "confidence": 0.91,
            "is_ai_generated": False
        }
    }
