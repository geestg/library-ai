from __future__ import annotations

from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)
from delbot_platform.knowledge.rag.models.response import (
    RAGResponse,
)


class RAGEngine:

    def __init__(
        self,
    ) -> None:

        self.pipeline = RAGPipeline()

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> RAGResponse:

        return await self.pipeline.build(
            query=query,
            retrieve_limit=limit,
        )
