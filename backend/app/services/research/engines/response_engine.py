from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# BUILD RESEARCH RESPONSE
# =====================================

def build_research_response(
    context: ResearchContext
):

    return {

        "query":
        context.query,

        "mode":
        context.mode,

        "related_theses":
        context.theses,

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
        context.trend_analysis,

        "competency_analysis":
        context.competency_analysis,

        "prodi_analysis":
        context.prodi_analysis,

        "analysis":
        context.analysis
    }