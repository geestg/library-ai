from app.services.research.intent_detector import (
    is_literature_review_query
)

from app.services.research.literature_review_generator import (
    generate_literature_review
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# CONFIG
# =====================================

MIN_THESIS_FOR_REVIEW = 5


# =====================================
# LITERATURE REVIEW PIPELINE
# =====================================

def run_literature_review_pipeline(
    context: ResearchContext
):

    if not is_literature_review_query(
        context.query
    ):
        return None

    # =================================
    # MINIMUM EVIDENCE CHECK
    # =================================

    if len(context.theses) < MIN_THESIS_FOR_REVIEW:

        return {

            "query":
            context.query,

            "mode":
            "literature_review",

            "analysis":
            (
                "Bukti penelitian tidak cukup "
                "untuk menghasilkan literature review "
                "yang valid.\n\n"
                f"Ditemukan hanya {len(context.theses)} "
                f"skripsi relevan, sedangkan minimal "
                f"{MIN_THESIS_FOR_REVIEW} sumber "
                "dibutuhkan untuk analisis yang "
                "lebih dapat dipercaya."
            ),

            "citations":
            context.citations,

            "evidence":
            context.evidence,

            "evidence_matrix":
            context.evidence_matrix,

            "gap_analysis":
            context.gap_analysis,

            "novelty_analysis":
            context.novelty_analysis,

            "trend_analysis":
            context.trend_analysis
        }

    # =================================
    # GENERATE REVIEW
    # =================================

    review_result = (
        generate_literature_review(

            query=
            context.query,

            evidence=
            context.evidence,

            evidence_matrix=
            context.evidence_matrix,

            gap_analysis=
            context.gap_analysis,

            citation_context=
            context.citation_context
        )
    )

    return {

        "query":
        context.query,

        "mode":
        "literature_review",

        "analysis":
        review_result[
            "literature_review"
        ],

        "citations":
        context.citations,

        "evidence":
        context.evidence,

        "evidence_matrix":
        context.evidence_matrix,

        "gap_analysis":
        context.gap_analysis,

        "novelty_analysis":
        context.novelty_analysis,

        "trend_analysis":
        context.trend_analysis
    }