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
    context: ResearchContext,
    stream: bool = False
):
    """
    Execute the LLM stage.

    REST MODE
    ---------
    stream=False

    Populate:
        context.analysis

    Return:
        ResearchContext

    STREAM MODE
    -----------
    stream=True

    Return:
        Generator[str, None, None]

    The caller is responsible for consuming the
    generator and building the streamed response.
    """

    # =================================
    # STREAM MODE
    # =================================

    if stream:

        return gateway.stream_response(

            prompt=context.prompt,

            model=context.model or None,

            provider=context.provider or None,
        )

    # =================================
    # NORMAL MODE
    # =================================

    context.analysis = gateway.generate_response(

        prompt=context.prompt,

        model=context.model or None,

        provider=context.provider or None,
    )

    return context