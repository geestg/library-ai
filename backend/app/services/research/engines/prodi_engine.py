from app.services.research.prodi.prodi_engine import (
    build_prodi_analysis
)

from app.services.research.models.research_context import (
    ResearchContext
)


def run_prodi_pipeline(
    context: ResearchContext
):

    context.prodi_analysis = (

        build_prodi_analysis(

            domain=
            context.final_domain.get(
                "domain",
                "general"
            ),

            competency_analysis=
            context.competency_analysis
        )
    )

    return context