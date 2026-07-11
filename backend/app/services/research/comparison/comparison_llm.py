from app.services.llm.tasks.llm_task import (
    LLMTask,
)


# =====================================
# COMPARISON ANALYSIS
# =====================================

def generate_comparison_analysis(
    prompt: str,
    model: str | None = None,
    provider: str | None = None,
):

    return LLMTask.answer(

        prompt=prompt,

        model=model,

        provider=provider,

    )