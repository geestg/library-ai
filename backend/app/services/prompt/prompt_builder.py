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

SOURCE_ID yang tersedia pada context
adalah satu-satunya sumber informasi.

Gunakan citation inline pada setiap
klaim faktual yang berasal dari context.

Format citation wajib:

[1]
[2]
[3]

Contoh:

"Penelitian sebelumnya menggunakan
CNN untuk klasifikasi citra [1]."

Jika sebuah pernyataan didukung
lebih dari satu sumber:

[1][2]

Jangan membuat citation yang tidak ada.

Jangan menggunakan nomor citation
di luar SOURCE_ID yang tersedia.

Jika informasi tidak ditemukan
pada source retrieval:

katakan secara eksplisit:

"Informasi tersebut tidak ditemukan
pada source yang tersedia."

Setiap bagian berikut harus memiliki
citation jika berisi fakta:

- Literature Review
- Metodologi
- Teknologi
- Research Gap
- Novelty
- Future Work

Prioritaskan evidence dibanding opini.

Jangan membuat klaim tanpa citation.

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