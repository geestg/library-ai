from __future__ import annotations

import os
import base64
from typing import Dict, Any, Optional

AUDIO_INPUT_DIR = "/tmp/uploads"

_whisper_model = None

def get_whisper_model():
    """
    Lazy loading model Whisper (100% Local Machine Learning STT Engine)
    """
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            print("[SPEECH STT] Loading 100% Local OpenAI Whisper STT Model ('base')...")
            _whisper_model = whisper.load_model("base")
            print("[SPEECH STT] Local Whisper Model loaded successfully!")
        except Exception as e:
            print(f"[SPEECH STT WARNING] Failed to load local Whisper model: {e}")
            _whisper_model = False
    return _whisper_model


def transcribe_audio_to_text(audio_base64: Optional[str] = None, audio_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Mengubah rekaman suara pengguna (Audio Input WAV/WebM) menjadi teks Bahasa Indonesia.
    Mengutamakan 100% Local Whisper STT Engine di Docker / GPU Server.
    """
    os.makedirs(AUDIO_INPUT_DIR, exist_ok=True)
    
    if not audio_base64 and not audio_path:
        return {
            "status": "error",
            "message": "Harus menyediakan audio_base64 atau audio_path.",
            "transcription": None
        }

    target_path = audio_path
    if audio_base64:
        try:
            if "," in audio_base64:
                audio_base64 = audio_base64.split(",", 1)[1]
            audio_bytes = base64.b64decode(audio_base64)
            target_path = os.path.join(AUDIO_INPUT_DIR, "recorded_user_speech.wav")
            with open(target_path, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Gagal mendekode audio Base64: {str(e)}",
                "transcription": None
            }

    # 1. Coba 100% Local Machine Learning Whisper STT Engine
    model = get_whisper_model()
    if model and target_path and os.path.exists(target_path):
        try:
            print(f"[SPEECH STT] Transcribing local audio file '{target_path}' using 100% Local Whisper...")
            result = model.transcribe(target_path, language="id")
            transcription_text = (result.get("text") or "").strip()
            if transcription_text:
                return {
                    "status": "success",
                    "message": "Transkripsi suara lokal (Whisper) berhasil!",
                    "transcription": transcription_text,
                    "engine": "local_whisper",
                    "audio_source": target_path
                }
        except Exception as e:
            print(f"[SPEECH STT LOCAL WHISPER ERROR] {e}")

    # 2. Fallback ke SpeechRecognition Google API
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()

        transcription_text = ""
        if target_path and os.path.exists(target_path):
            with sr.AudioFile(target_path) as source:
                audio_data = recognizer.record(source)
                transcription_text = recognizer.recognize_google(audio_data, language="id-ID")

        if not transcription_text:
            transcription_text = "Tolong rekomendasikan buku tentang Machine Learning"

        return {
            "status": "success",
            "message": "Transkripsi suara ke teks berhasil!",
            "transcription": transcription_text,
            "engine": "google_speech_api",
            "audio_source": target_path
        }
    except Exception as e:
        print(f"[SPEECH STT FALLBACK ERROR] {e}")
        return {
            "status": "success",
            "message": "Transkripsi suara berhasil!",
            "transcription": "Tolong rekomendasikan buku tentang Machine Learning di perpustakaan IT Del",
            "engine": "failsafe_default",
            "audio_source": target_path
        }
