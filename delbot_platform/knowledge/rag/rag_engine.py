from __future__ import annotations

from delbot_platform.knowledge.models import RAGResult
from delbot_platform.knowledge.rag.pipeline import (
    RAGPipeline,
)


class RAGEngine:

    def __init__(
        self,
    ) -> None:

        self.pipeline = RAGPipeline()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> RAGResult:

        return self.pipeline.search(
            query=query,
            limit=limit,
        )
