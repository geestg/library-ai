from app.services.research.domain_classifier import (
    detect_domain
)

from app.services.research.domain_resolver import (
    resolve_domain
)

from app.services.research.domain_prompts import (
    get_domain_instruction
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# DOMAIN PIPELINE
# =====================================

def run_domain_pipeline(
    context: ResearchContext
):

    context.query_domain = (
        detect_domain(
            context.query
        )
    )

    context.final_domain = (
        resolve_domain(

            context.query_domain,

            context.theses
        )
    )

    context.domain_instruction = (
        get_domain_instruction(
            context.final_domain.get(
                "domain",
                "general"
            )
        )
    )

    print(
        "\n===================================="
    )

    print(
        "DOMAIN PIPELINE"
    )

    print(
        "===================================="
    )

    print(
        context.final_domain
    )

    return context
