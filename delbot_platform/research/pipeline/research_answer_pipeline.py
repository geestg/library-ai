from __future__ import annotations

import inspect

from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)

from delbot_platform.research.generator import (
    LLMGenerator,
)

from delbot_platform.research.models import (
    ResearchPipelineResponse,
)

from delbot_platform.research.prompt_builder import (
    ResearchPromptBuilder,
)


class ResearchAnswerPipeline:

    def __init__(
        self,
    ) -> None:

        self.rag = None

        self.prompt_builder = (
            ResearchPromptBuilder()
        )

        self.generator = (
            LLMGenerator()
        )

    def get_rag(
        self,
    ) -> RAGPipeline:

        if self.rag is None:

            self.rag = RAGPipeline()

        return self.rag

    async def answer(
        self,
        *,
        question: str,
        history: list[dict] | None = None,
        previous: str = "",
        research_state: dict | None = None,
    ) -> ResearchPipelineResponse:

        history = history or []

        research_state = (
            research_state or {}
        )

        rag = await self.get_rag().build(
            query=question,
        )

        messages = (
            self.prompt_builder.build(
                query=question,
                context=rag.context,
                history=history,
                previous=previous,
                research_state=research_state,
            )
        )

        generated = self.generator.generate(
            messages,
        )

        if inspect.isawaitable(
            generated
        ):
            generated = await generated

        return ResearchPipelineResponse(
            answer=generated,
            citations=rag.citations,
            rag=rag,
        )
