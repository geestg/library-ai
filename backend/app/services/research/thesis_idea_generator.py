from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)

from app.services.research.models.research_context import (
    ResearchContext,
)


# =====================================
# THESIS IDEA GENERATOR
# =====================================

def generate_thesis_ideas(
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
NOVELTY ANALYSIS
==================================================

{profile.novelty.to_dict()}

==================================================
COMPETENCY ANALYSIS
==================================================

{profile.competency.to_dict()}

==================================================
PROGRAM STUDY ANALYSIS
==================================================

{profile.prodi.to_dict()}

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

1.
Gunakan hanya evidence yang tersedia.

2.
Prioritaskan:

- Method Gap

- Dataset Gap

- Evaluation Gap

3.
Jangan membuat teknologi baru.

4.
Jangan membuat dataset baru.

5.
Jangan membuat metodologi baru.

6.
Gunakan Bahasa Indonesia akademik.

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

dst.
"""

    request = PromptRequest(

        prompt=prompt,

        model=context.model,

        provider=context.provider,

    )

    ideas = LLMTask.creative(
        request
    )

    return {

        "query":
            context.query,

        "ideas":
            ideas,

        "novelty_score":
            profile.novelty.novelty_score,

        "novelty_level":
            profile.novelty.novelty_level,

    }

