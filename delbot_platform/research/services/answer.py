from __future__ import annotations

from delbot_platform.knowledge.rag.research.pipeline import (
    ResearchAnswerPipeline,
)
from delbot_platform.knowledge.rag.research.response import (
    ResearchPipelineResponse,
)


class ResearchAnswerService:
    """
    Canonical Research Answer Service.
    """

    def __init__(
        self,
    ) -> None:

        self.pipeline = ResearchAnswerPipeline()

    async def answer(
        self,
        *,
        question: str,
    ) -> ResearchPipelineResponse:

        return await self.pipeline.answer(
            question=question,
        )
