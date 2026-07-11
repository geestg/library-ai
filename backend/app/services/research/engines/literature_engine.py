from app.services.research.intent_detector import (
    is_literature_review_query,
)

from app.services.research.literature_review_generator import (
    generate_literature_review,
)

from app.services.research.models.research_context import (
    ResearchContext,
)


# =====================================
# CONFIG
# =====================================

MIN_THESIS_FOR_REVIEW = 5


# =====================================
# BUILD RESPONSE
# =====================================

def build_response(
    context: ResearchContext,
    analysis: str,
):

    profile = (
        context.research_profile
    )

    profile_dict = (
        profile.to_dict()
    )

    response = {

        # =================================
        # REQUEST
        # =================================

        "query":
        context.query,

        "mode":
        "literature_review",

        # =================================
        # LLM
        # =================================

        "provider":
        context.provider,

        "model":
        context.model,

        "intent":
        context.intent,

        # =================================
        # RESPONSE
        # =================================

        "analysis":
        analysis,

        # =================================
        # DOMAIN MODEL
        # =================================

        "research_profile":
        profile_dict,

        # =================================
        # RETRIEVAL
        # =================================

        "citations":
        context.citations,

        "related_theses":
        context.theses,

        # =================================
        # EVIDENCE
        # =================================

        "evidence":
        context.evidence,

        "evidence_matrix":
        context.evidence_matrix,

    }

    # =====================================
    # LEGACY COMPATIBILITY
    # =====================================

    response.update({

        "trend_analysis":
        profile_dict["trend"],

        "gap_analysis":
        profile_dict["gap"],

        "novelty_analysis":
        profile_dict["novelty"],

        "competency_analysis":
        profile_dict["competency"],

        "prodi_analysis":
        profile_dict["prodi"],

    })

    return response


# =====================================
# LITERATURE REVIEW PIPELINE
# =====================================

def run_literature_review_pipeline(
    context: ResearchContext,
):

    if not is_literature_review_query(
        context.query
    ):
        return None

    # =================================
    # MINIMUM EVIDENCE CHECK
    # =================================

    if len(context.theses) < MIN_THESIS_FOR_REVIEW:

        return build_response(

            context,

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

        )

    # =================================
    # GENERATE REVIEW
    # =================================

    review = (
        generate_literature_review(
            context
        )
    )

    return build_response(

        context,

        review[
            "literature_review"
        ],

    )
