from pydantic import BaseModel, HttpUrl

class VoiceRequest(BaseModel):
    request_description: str
    audio_url: HttpUrl
