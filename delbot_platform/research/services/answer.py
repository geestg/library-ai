from __future__ import annotations

from delbot_platform.research.pipeline import (
    ResearchAnswerPipeline,
)
from delbot_platform.research.models import (
    ResearchPipelineResponse,
)


class ResearchAnswerService:
    """
    Canonical Research Answer Service.
    """

    def __init__(
        self,
    ) -> None:

        self.pipeline = None


    def get_pipeline(
        self,
    ) -> ResearchAnswerPipeline:

        if self.pipeline is None:
            self.pipeline = ResearchAnswerPipeline()

        return self.pipeline

    async def answer(
        self,
        *,
        question: str,
    ) -> ResearchPipelineResponse:

        return await self.get_pipeline().answer(
            question=question,
        )