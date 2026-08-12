from __future__ import annotations

from abc import ABC
from abc import abstractmethod


from delbot_platform.knowledge.retrieval.result import (
    RetrievalResult,
)


class Retriever(ABC):


    @abstractmethod
    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        document_ids: list[str] | None = None,
    ) -> list[RetrievalResult]:

        pass