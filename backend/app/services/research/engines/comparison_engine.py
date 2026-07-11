from app.services.research.method_comparison_engine import (
    is_comparison_query,
    run_method_comparison
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# COMPARISON PIPELINE
# =====================================

def run_comparison_pipeline(
    context: ResearchContext
):

    if not is_comparison_query(
        context.query
    ):
        return None

    result = (
        run_method_comparison(

            query=context.query,

            theses=context.theses
        )
    )

    return {

        "query":
        context.query,

        "mode":
        "comparison",

        "related_theses":
        context.theses,

        "citations":
        context.citations,

        "comparison_matrix":
        result.get(
            "comparison_matrix",
            {}
        ),

        "comparison":
        result.get(
            "comparison",
            ""
        ),

        "analysis":
        result.get(
            "comparison",
            ""
        )
    }
