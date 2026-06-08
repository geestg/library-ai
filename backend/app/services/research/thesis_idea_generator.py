from app.services.llm.model_gateway import (
    gateway
)

# =====================================
# THESIS IDEA GENERATOR
# =====================================

def generate_thesis_ideas(

    query: str,

    evidence: dict,

    evidence_matrix: dict,

    gap_analysis: dict,

    novelty_analysis: dict
):

    prompt = f"""
Anda adalah DELBot.

Asisten Riset Akademik.

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
NOVELTY
==================================================

{novelty_analysis}

==================================================
TUGAS
==================================================

Buat 5 ide skripsi terbaik.

Setiap ide wajib memiliki:

1. Judul
2. Research Gap
3. Novelty
4. Metode
5. Dataset
6. Kontribusi
7. Tingkat Kesulitan

==================================================
ATURAN
==================================================

1. Gunakan hanya informasi yang tersedia.

2. Prioritaskan area yang memiliki:

- Method Gap
- Dataset Gap
- Evaluation Gap

3. Hindari topik yang terlalu umum.

4. Hindari novelty palsu.

5. Gunakan Bahasa Indonesia akademik.

==================================================
FORMAT
==================================================

# Ide 1

Judul:

Gap:

Novelty:

Metode:

Dataset:

Kontribusi:

Kesulitan:

# Ide 2

dst
"""

    result = gateway.generate_response(
        prompt=prompt
    )

    return {

        "query":
        query,

        "ideas":
        result,

        "novelty_score":
        novelty_analysis.get(
            "novelty_score",
            0
        ),

        "novelty_level":
        novelty_analysis.get(
            "novelty_level",
            "LOW"
        )
    }