from app.services.research.prodi.prodi_engine import (
    build_prodi_analysis,
)

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.models.prodi_analysis import (
    ProdiAnalysis,
)


# =====================================
# PRODI PIPELINE
# =====================================

def run_prodi_pipeline(
    context: ResearchContext,
):

    # =================================
    # BUILD PRODI ANALYSIS
    # =================================

    competency_payload = {

        "competencies": [

            competency.to_dict()

            for competency in (
                context
                .research_profile
                .competency
                .competencies
            )

        ]

    }

    prodi_result = (

        build_prodi_analysis(

            domain=
            context.final_domain.get(
                "domain",
                "general",
            ),

            competency_analysis=
            competency_payload,

        )

    )

    # =================================
    # RESEARCH PROFILE
    # =================================

    context.research_profile.prodi = (

        ProdiAnalysis(

            prodi=prodi_result.get(
                "prodi",
                "",
            ),

            focus_areas=prodi_result.get(
                "focus_areas",
                [],
            ),

            dominant_competencies=prodi_result.get(
                "dominant_competencies",
                [],
            ),

            matched_competencies=prodi_result.get(
                "matched_competencies",
                [],
            ),

            research_alignment=prodi_result.get(
                "research_alignment",
                0.0,
            ),

        )

    )



    return context
