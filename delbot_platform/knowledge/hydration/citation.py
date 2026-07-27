from __future__ import annotations

from delbot_platform.knowledge.hydration.base import (
    DocumentProvider,
)
from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)
from delbot_platform.research.models import (
    Citation,
)


class CitationHydrator:

    def __init__(
        self,
        provider: DocumentProvider,
    ) -> None:

        self.provider = provider

    async def hydrate(
        self,
        result: RerankResult,
    ) -> Citation:

        metadata = result.metadata

        return await self.provider.citation(
            document_id=metadata.document_id,
            page_start=metadata.page_start,
            page_end=metadata.page_end,
            section=metadata.section,
            text=result.content,
        )

    async def hydrate_many(
        self,
        results: list[RerankResult],
    ) -> list[Citation]:

        citations: list[Citation] = []

        for result in results:

            citations.append(
                await self.hydrate(
                    result,
                )
            )

        return citations
