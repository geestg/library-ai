from __future__ import annotations

from typing import Dict, Any, Optional
from app.services.speech.tts_service import synthesize_text_to_speech
from app.services.speech.stt_service import transcribe_audio_to_text


class SpeechService:
    """
    Service Facade Utama untuk mengelola fitur Suara (Voice Assistant / Text-to-Speech / Speech-to-Text) DELBot.
    """

    def text_to_speech(self, text: str, lang: str = "id") -> Dict[str, Any]:
        """
        Sintesis Teks Jawaban DELBot ke Suara (TTS).
        """
        return synthesize_text_to_speech(text, lang=lang)

    def speech_to_text(self, audio_base64: Optional[str] = None, audio_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Transkripsi Suara Pertanyaan Mahasiswa ke Teks (STT).
        """
        return transcribe_audio_to_text(audio_base64=audio_base64, audio_path=audio_path)


# Instance Global
speech_service = SpeechService()
