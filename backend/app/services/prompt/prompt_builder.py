from app.services.prompt.response_modes import (
    RESPONSE_MODES
)


# =====================================
# DETECT RESPONSE MODE
# =====================================

def detect_response_mode(query: str):

    query_lower = query.lower()

    # =====================================
    # RESEARCH GAP
    # =====================================

    if any(word in query_lower for word in [

        "research gap",

        "gap penelitian",

        "novelty",

        "future work"

    ]):

        return "research_gap"

    # =====================================
    # METHODOLOGY
    # =====================================

    if any(word in query_lower for word in [

        "metodologi",

        "metode",

        "algoritma",

        "framework"

    ]):

        return "methodology"

    # =====================================
    # LITERATURE REVIEW
    # =====================================

    if any(word in query_lower for word in [

        "literature review",

        "state of the art",

        "penelitian sebelumnya",

        "related work"

    ]):

        return "literature"

    # =====================================
    # TECHNICAL
    # =====================================

    if any(word in query_lower for word in [

        "arsitektur",

        "transformer",

        "cnn",

        "svm",

        "fine tuning",

        "embedding"

    ]):

        return "technical"

    # =====================================
    # DEFAULT
    # =====================================

    return "academic"


# =====================================
# BUILD PROMPT
# =====================================

def build_prompt(

    query: str,

    context: str,

    intent: str

):

    # =====================================
    # RESPONSE MODE
    # =====================================

    mode = detect_response_mode(
        query
    )

    mode_instruction = RESPONSE_MODES[
        mode
    ]

    # =====================================
    # PROMPT
    # =====================================

    prompt = f"""
Kamu adalah DELBot,
AI Academic Knowledge Operating System.

Kamu membantu:
- penelitian akademik
- semantic retrieval
- literature review
- analisis metodologi
- research insight
- academic reasoning

====================================
MODE RESPONSE
====================================

{mode}

====================================
STYLE INSTRUCTION
====================================

{mode_instruction}

====================================
INTENT USER
====================================

{intent}

====================================
KONTEKS AKADEMIK
====================================

{context}

====================================
PERTANYAAN USER
====================================

{query}

====================================
ATURAN JAWABAN
====================================

- Jawab dalam Bahasa Indonesia
- Jangan halusinasi
- Fokus pada konteks retrieval
- Gunakan reasoning akademik
- Berikan insight jika relevan
- Jika konteks kurang relevan, katakan dengan jujur
- Jangan terlalu verbose
- Gunakan struktur yang rapi

====================================
ATURAN CITATION
====================================

- Gunakan citation inline menggunakan format:
  [1], [2], [3], dst

- Gunakan hanya citation yang tersedia
  berdasarkan SOURCE_ID pada context

- Jangan membuat citation palsu

- Jika mengambil insight dari source tertentu,
  tambahkan citation di akhir kalimat

Contoh:
"Hybrid retrieval meningkatkan relevansi pencarian [1]."

- Jika beberapa source mendukung
  satu pernyataan, gunakan:
  [1][2]

- Jangan gunakan citation jika
  informasi tidak tersedia pada context

====================================
TUJUAN UTAMA
====================================

Berikan jawaban akademik yang:
- grounded
- evidence-aware
- jelas
- terstruktur
- dapat ditelusuri sumbernya
"""

    return prompt