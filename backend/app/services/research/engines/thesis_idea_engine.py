from app.services.research.intent_detector import (
    is_thesis_idea_query
)

from app.services.research.thesis_idea_generator import (
    generate_thesis_ideas
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# THESIS IDEA PIPELINE
# =====================================

def run_thesis_idea_pipeline(
    context: ResearchContext
):

    if not is_thesis_idea_query(
        context.query
    ):
        return None

    idea_result = (
        generate_thesis_ideas(

            query=
            context.query,

            evidence=
            context.evidence,

            evidence_matrix=
            context.evidence_matrix,

            gap_analysis=
            context.gap_analysis,

            novelty_analysis=
            context.novelty_analysis
        )
    )

    return {

        "query":
        context.query,

        "mode":
        "thesis_ideas",

        "analysis":
        idea_result["ideas"],

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