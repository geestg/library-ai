from app.services.prompts.registry import (
    PromptRegistry,
)

from app.services.prompts.models.prompt_type import (
    PromptType,
)

from app.services.prompts.answer.answer_prompt import (
    AnswerPrompt,
)

from app.services.prompts.document.document_prompt import (
    DocumentPrompt,
)

from app.services.prompts.verifier.verifier_prompt import (
    VerifierPrompt,
)

from app.services.prompts.query_resolution.query_resolution_prompt import (
    QueryResolutionPrompt,
)

from app.services.prompts.research.research_prompt import (
    ResearchPrompt,
)

from app.services.prompts.creative.creative_prompt import (
    CreativePrompt,
)

from app.services.prompts.title.title_prompt import (
    TitlePrompt,
)


def register_prompts():

    PromptRegistry.register(
        PromptType.ANSWER,
        AnswerPrompt,
    )

    PromptRegistry.register(
        PromptType.DOCUMENT,
        DocumentPrompt,
    )

    PromptRegistry.register(
        PromptType.VERIFIER,
        VerifierPrompt,
    )

    PromptRegistry.register(
        PromptType.QUERY_RESOLUTION,
        QueryResolutionPrompt,
    )

    PromptRegistry.register(
        PromptType.RESEARCH,
        ResearchPrompt,
    )

    PromptRegistry.register(
        PromptType.CREATIVE,
        CreativePrompt,
    )

    PromptRegistry.register(
        PromptType.TITLE,
        TitlePrompt,
    )