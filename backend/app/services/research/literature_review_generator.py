from app.services.llm.model_gateway import (
    gateway
)

# =====================================
# LITERATURE REVIEW GENERATOR
# =====================================

def generate_literature_review(

    query: str,

    evidence: dict,

    evidence_matrix: dict,

    gap_analysis: dict,

    citation_context: str
):

    prompt = f"""
Anda adalah DELBot.

Asisten Akademik Institut Teknologi Del.

==================================================
TOPIK
==================================================

{query}

==================================================
EVIDENCE
==================================================

{evidence}

==================================================
EVIDENCE MATRIX
==================================================

{evidence_matrix}

==================================================
RESEARCH GAP
==================================================

{gap_analysis}

==================================================
SUMBER
==================================================

{citation_context}

==================================================
TUGAS
==================================================

Buat Tinjauan Pustaka Akademik.

Gunakan hanya sumber yang tersedia.

==================================================
FORMAT
==================================================

# Pendahuluan

# Penelitian Terdahulu

# Analisis Perbandingan Penelitian

# Research Gap

# Posisi Penelitian Yang Diusulkan

# Kesimpulan

==================================================
ATURAN
==================================================

1. Semua klaim wajib memiliki sitasi.

2. Format sitasi:

[1]
[2]
[3]

3. Jangan membuat sumber baru.

4. Jangan mengarang teknologi.

5. Jangan mengarang metodologi.

6. Bahasa Indonesia akademik.
"""

    review = gateway.generate_response(
        prompt=prompt
    )

    return {

        "query":
        query,

        "literature_review":
        review
    }