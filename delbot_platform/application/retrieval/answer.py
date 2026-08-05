from __future__ import annotations

from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)

from delbot_platform.knowledge.rag.models.response import (
    RAGResponse,
)


class RetrievalApplication:
    """
    Canonical Retrieval Application.

    Thin application layer for the MVP.

    API
        ↓
    RetrievalApplication
        ↓
    RAGPipeline
    """

    def __init__(
        self,
    ) -> None:

        self.pipeline: RAGPipeline | None = None

    def get_pipeline(
        self,
    ) -> RAGPipeline:

        if self.pipeline is None:
            self.pipeline = RAGPipeline()

        return self.pipeline

    async def execute(
        self,
        *,
        question: str,
        retrieve_limit: int = 20,
        rerank_limit: int = 5,
    ) -> RAGResponse:

        return await self.get_pipeline().build(
            query=question,
            retrieve_limit=retrieve_limit,
            rerank_limit=rerank_limit,
        )
