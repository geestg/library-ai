from app.services.research.prompt_builder import (
    build_research_prompt
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# PROMPT PIPELINE
# =====================================

def run_prompt_pipeline(
    context: ResearchContext
):

    context.prompt = (
        build_research_prompt(

            query=
            context.query,

            evidence_text=
            context.combined_evidence,

            citation_context=
            context.citation_context,

            domain_instruction=
            context.domain_instruction,

            mode=
            context.mode
        )
    )

    print("\n====================================")
    print("PROMPT GENERATED")
    print("====================================")

    return context