from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, Dict, Any


class TTSRequest(BaseModel):
    text: str
    lang: Optional[str] = "id"


class STTRequest(BaseModel):
    audio_base64: Optional[str] = None
    audio_path: Optional[str] = None
