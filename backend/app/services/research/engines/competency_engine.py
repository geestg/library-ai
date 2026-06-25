from app.services.research.competency.competency_engine import (
    build_competencies
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# COMPETENCY PIPELINE
# =====================================

def run_competency_pipeline(
    context: ResearchContext
):

    context.competency_analysis = {

        "competencies":

        build_competencies(

            context.evidence
        )
    }

    return context