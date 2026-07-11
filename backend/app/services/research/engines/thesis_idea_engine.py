from app.services.research.intent_detector import (
    is_thesis_idea_query,
)

from app.services.research.thesis_idea_generator import (
    generate_thesis_ideas,
)

from app.services.research.models.research_context import (
    ResearchContext,
)


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
        "thesis_ideas",

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

        "related_theses":
        context.theses,

        "citations":
        context.citations,

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
    # -------------------------------------
    # Remove after REST frontend
    # fully migrates to
    # research_profile.
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
# THESIS IDEA PIPELINE
# =====================================

def run_thesis_idea_pipeline(
    context: ResearchContext,
):

    if not is_thesis_idea_query(
        context.query
    ):
        return None

    idea_result = (
        generate_thesis_ideas(
            context
        )
    )

    return build_response(

        context,

        idea_result[
            "ideas"
        ],

    )
