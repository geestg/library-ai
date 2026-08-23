from __future__ import annotations

import os
import re
import uuid
import base64
from typing import Dict, Any, Optional

AUDIO_OUTPUT_DIR = "/tmp/uploads/reports"


def clean_text_for_speech(text: str) -> str:
    """
    Membersihkan simbol-simbol Markdown, emoji, dan format kaku
    agar ucapan suara TTS terdengar alami dan halus dalam Bahasa Indonesia.
    """
    if not text:
        return ""
    
    # Hapus Markdown bold, italic, code block, header
    clean = re.sub(r'[*_`#~]', '', text)
    # Hapus emoji & simbol spesial
    clean = re.sub(r'[📖📍👤📝🏷️⚠️🚀📁📁🔴🟢💡🎯❓🛡️]', '', clean)
    # Hapus URL
    clean = re.sub(r'http\S+', '', clean)
    # Gantikan baris baru dengan koma/jeda
    clean = re.sub(r'\n+', '. ', clean)
    # Rapikan spasi ganda
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean[:1000]  # Batasi 1000 karakter per sintesis suara agar cepat


def synthesize_text_to_speech(text: str, lang: str = "id", slow: bool = False) -> Dict[str, Any]:
    """
    Mengubah teks jawaban DELBot menjadi audio MP3 suara Bahasa Indonesia alami.
    """
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    clean_prompt = clean_text_for_speech(text)
    
    if not clean_prompt:
        return {
            "status": "error",
            "message": "Teks kosong, tidak dapat menyintesis suara.",
            "audio_url": None,
            "audio_base64": None
        }

    try:
        from gtts import gTTS
        tts = gTTS(text=clean_prompt, lang=lang, slow=slow)
        
        filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)
        tts.save(filepath)
        
        with open(filepath, "rb") as f:
            audio_bytes = f.read()
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            
        audio_url = f"/reports/{filename}"
        
        return {
            "status": "success",
            "message": "Sintesis suara berhasil!",
            "filename": filename,
            "audio_url": audio_url,
            "audio_base64": audio_b64,
            "text_spoken": clean_prompt
        }
    except Exception as e:
        print(f"[SPEECH TTS ERROR] {e}")
        return {
            "status": "error",
            "message": f"Gagal menyintesis suara: {str(e)}",
            "audio_url": None,
            "audio_base64": None
        }
