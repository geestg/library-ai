from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.prompts.models.prompt_request import (
    PromptRequest,
)


# =====================================
# COMPARISON ANALYSIS
# =====================================

def generate_comparison_analysis(
    prompt: str,
    model: str | None = None,
    provider: str | None = None,
):

    request = PromptRequest(

        prompt=prompt,

        model=model,

        provider=provider,

    )

    return LLMTask.answer(
        request
    )
