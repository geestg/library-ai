from __future__ import annotations

from fastapi import APIRouter, HTTPException
from delbot_platform.api.schemas.speech import TTSRequest, STTRequest
from delbot_platform.ai.speech import speech_service

router = APIRouter(
    prefix="/api/speech",
    tags=["Speech"],
)


@router.post("/tts")
async def text_to_speech_route(request: TTSRequest):
    """
    Sintesis Teks ke Suara Bahasa Indonesia (TTS).
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Teks tidak boleh kosong.")
    
    result = speech_service.text_to_speech(text=request.text, lang=request.lang or "id")
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result


@router.post("/stt")
async def speech_to_text_route(request: STTRequest):
    """
    Transkripsi Rekaman Suara ke Teks (STT).
    """
    if not request.audio_base64 and not request.audio_path:
        raise HTTPException(status_code=400, detail="Harus mengirimkan audio_base64 atau audio_path.")
    
    result = speech_service.speech_to_text(audio_base64=request.audio_base64, audio_path=request.audio_path)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result


from fastapi import APIRouter

from delbot_platform.api.schemas.vision import VisionChatRequest
from delbot_platform.ai.vision.vision_service import vision_chat

router = APIRouter(
    prefix="/api/vision",
    tags=["Vision"],
)


@router.post("/chat")
async def vision_chat_route(request: VisionChatRequest):
    return vision_chat(
        prompt=request.prompt,
        image_base64=request.image_base64,
        image_url=request.image_url,
    )
