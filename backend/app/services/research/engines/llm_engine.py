from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.research.models.research_context import (
    ResearchContext,
)


# =====================================
# LLM PIPELINE
# =====================================

def run_llm_pipeline(
    context: ResearchContext,
    stream: bool = False,
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

        return LLMTask.stream_answer(

            prompt=context.prompt,

            model=context.model,

            provider=context.provider,

        )

    # =================================
    # NORMAL MODE
    # =================================

    context.analysis = LLMTask.answer(

        prompt=context.prompt,

        model=context.model,

        provider=context.provider,

    )

    return context