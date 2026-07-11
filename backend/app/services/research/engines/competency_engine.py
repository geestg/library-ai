from app.services.research.competency.competency_engine import (
    build_competencies,
)

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.models.competency_analysis import (
    CompetencyAnalysis,
    CompetencyItem,
)


# =====================================
# COMPETENCY PIPELINE
# =====================================

def run_competency_pipeline(
    context: ResearchContext,
):

    # =================================
    # BUILD COMPETENCIES
    # =================================

    items = [

        CompetencyItem.from_dict(
            item
        )

        for item in build_competencies(
            context.evidence
        )

    ]

    # =================================
    # DOMINANT COMPETENCY
    # =================================

    dominant = ""

    if items:

        dominant = items[0].name

    # =================================
    # RESEARCH PROFILE
    # =================================

    context.research_profile.competency = (

        CompetencyAnalysis(

            competencies=items,

            total_competencies=len(
                items
            ),

            dominant_competency=dominant,

        )

    )



    return context
