from __future__ import annotations

from delbot_platform.ai.speech.speech_service import SpeechService, speech_service
from delbot_platform.ai.speech.tts_service import synthesize_text_to_speech
from delbot_platform.ai.speech.stt_service import transcribe_audio_to_text

__all__ = [
    "SpeechService",
    "speech_service",
    "synthesize_text_to_speech",
    "transcribe_audio_to_text",
]
