from app.services.llm.model_gateway import (
    gateway
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# LLM PIPELINE
# =====================================

def run_llm_pipeline(
    context: ResearchContext
):

    context.analysis = (
        gateway.generate_response(
            prompt=context.prompt
        )
    )

    return context