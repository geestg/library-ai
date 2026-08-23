from __future__ import annotations

from abc import ABC
from abc import abstractmethod


from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)



class Reranker(ABC):


    @abstractmethod
    async def rerank(
        self,
        query: str,
        documents: list[RerankResult],
        limit: int = 5,
    ) -> list[RerankResult]:

        pass