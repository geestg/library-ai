from __future__ import annotations

import re
from typing import Tuple


# =========================================
# SYSTEM SECURITY & CONTEXT GUARDRAILS
# =========================================
# Pattern untuk mendeteksi upaya jailbreak atau manipulasi sistem prompt (Prompt Injection)
JAILBREAK_PATTERNS = [
    r"\babaikan\s+(instruksi|perintah|aturan)\b",
    r"\bignore\s+(previous|rules|instructions)\b",
    r"\bsystem\s*prompt\b",
    r"\bdeveloper\s*mode\b",
    r"\bkamu\s+sekarang\s+adalah\b",
    r"\byou\s+are\s+now\s+a\b",
    r"\bacting\s+as\b",
    r"\bbypass\b",
    r"\bprompt\s+injection\b",
]

# Pattern untuk mendeteksi topik di luar konteks akademik perpustakaan IT Del
OUT_OF_CONTEXT_PATTERNS = [
    # 1. Permintaan coding/pemrograman umum (mengizinkan kata penengah seperti "buatkan saya coding")
    r"\b(buatkan|tuliskan|bikin|buat)\b.*\b(coding|program|script|code|aplikasi)\b",
    # 2. Resep masakan
    r"\b(resep|resep\s+masakan|resep\s+makanan)\b",
    r"\b(cara)\b.*\b(memasak|membuat\s+makanan|membuat\s+kue)\b",
    # 3. Topik hiburan/game
    r"\b(cheat|trik|cara\s+hack)\b.*\b(game|permainan)\b",
    # 4. Penerjemahan umum
    r"\b(terjemahkan|translate)\b.*\b(kalimat|paragraf|artikel|dokumen)\b",
]


def validate_query_safety(query: str) -> Tuple[bool, str]:
    """
    Validasi kueri dari ancaman prompt injection dan pembatasan konteks akademik perpustakaan.
    """
    normalized = query.lower().strip()

    # 1. Cek Upaya Prompt Injection / Jailbreak
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, normalized):
            print(f"[SECURITY GUARDRAILS] Terdeteksi potensi Prompt Injection: '{query}'")
            return False, (
                "Sistem mendeteksi adanya instruksi yang tidak sah. "
                "Sebagai AI Asisten Perpustakaan IT Del, saya tidak diizinkan untuk mengubah "
                "atau mengabaikan instruksi keamanan sistem."
            )
    # 2. Cek Kueri di Luar Konteks (Out of Context)
    for pattern in OUT_OF_CONTEXT_PATTERNS:
        if re.search(pattern, normalized):
            print(f"[SECURITY GUARDRAILS] Terdeteksi kueri di luar konteks: '{query}'")
            return False, (
                "Maaf, pertanyaan Anda di luar konteks perpustakaan dan akademik IT Del. "
                "Saya hanya dapat membantu menjawab pertanyaan seputar katalog buku, letak rak, "
                "informasi operasional perpustakaan, atau pencarian tugas akhir/skripsi."
            )
    return True, ""
