from __future__ import annotations

from delbot_platform.knowledge.rag.research.response import (
    ResearchPipelineResponse,
)

from delbot_platform.research.services import (
    ResearchAnswerService,
)


class ResearchAnswerApplication:
    """
    Research answering use case.
    """

    def __init__(
        self,
        service: ResearchAnswerService | None = None,
    ) -> None:

        self.service = (
            service
            if service is not None
            else ResearchAnswerService()
        )

    async def execute(
        self,
        question: str,
    ) -> ResearchPipelineResponse:

        return await self.service.answer(
            question=question,
        )