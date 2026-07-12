from typer import prompt

from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)

from app.services.research.models.research_context import (
    ResearchContext,
)
from app.services.prompts.models.prompt_type import PromptType


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
    # BUILD REQUEST
    # =================================

    PromptRequest.answer(
        prompt,
        model=model,
        provider=provider,
        prompt_type=PromptType.ANSWER,
    )
    
    # =================================
    # STREAM MODE
    # =================================

    if stream:

        return LLMTask.execute(
            request
        )

    # =================================
    # NORMAL MODE
    # =================================

    context.analysis = LLMTask.execute(
        request
    )

    return context


