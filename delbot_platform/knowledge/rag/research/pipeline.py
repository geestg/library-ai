from __future__ import annotations

from delbot_platform.knowledge.rag.llm.generator import (
    LLMGenerator,
)
from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)
from delbot_platform.knowledge.rag.research.response import (
    ResearchPipelineResponse,
)


class ResearchAnswerPipeline:

    def __init__(
        self,
    ) -> None:

        self.rag = RAGPipeline()

        self.generator = LLMGenerator()

    async def answer(
        self,
        question: str,
    ) -> ResearchPipelineResponse:

        rag_response = await self.rag.build(
            query=question,
        )

        llm = await self.generator.generate(
            context=rag_response.context,
            citations=rag_response.citations,
            instruction=question,
        )

        return ResearchPipelineResponse(
            answer=llm.answer,
            citations=llm.citations,
            rag=rag_response,
        )