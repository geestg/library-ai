from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.research.models.research_context import (
    ResearchContext,
)


# =====================================
# LITERATURE REVIEW GENERATOR
# =====================================

def generate_literature_review(
    context: ResearchContext,
):

    profile = context.research_profile

    prompt = f"""
Anda adalah DELBot.

Academic Intelligence System Institut Teknologi Del.

==================================================
TOPIK
==================================================

{context.query}

==================================================
EVIDENCE
==================================================

{context.evidence}

==================================================
EVIDENCE MATRIX
==================================================

{context.evidence_matrix}

==================================================
TREND ANALYSIS
==================================================

{profile.trend.to_dict()}

==================================================
RESEARCH GAP
==================================================

{profile.gap.to_dict()}

==================================================
NOVELTY
==================================================

{profile.novelty.to_dict()}

==================================================
COMPETENCY
==================================================

{profile.competency.to_dict()}

==================================================
PROGRAM STUDY
==================================================

{profile.prodi.to_dict()}

==================================================
SUMBER
==================================================

{context.citation_context}

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

# Analisis Perbandingan

# Research Gap

# Posisi Penelitian

# Kesimpulan

==================================================
ATURAN
==================================================

1.
Semua klaim wajib memiliki sitasi.

2.
Format sitasi:

[1]
[2]
[3]

3.
Jangan membuat sumber baru.

4.
Jangan mengarang teknologi.

5.
Jangan mengarang metodologi.

6.
Gunakan hanya evidence yang tersedia.

7.
Gunakan Bahasa Indonesia akademik.
"""

    review = LLMTask.research(

        prompt=prompt,

        model=context.model,

        provider=context.provider,

    )

    return {

        "query":
            context.query,

        "literature_review":
            review,

    }