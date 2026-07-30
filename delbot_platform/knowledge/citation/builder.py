from __future__ import annotations

from delbot_platform.knowledge.citation.source import (
    CitationSource,
)
from delbot_platform.knowledge.reranking.result import (
    RerankResult,
)


class CitationBuilder:

    def build(
        self,
        results: list[RerankResult],
    ) -> list[CitationSource]:

        citations: list[CitationSource] = []

        for item in results:

            metadata = item.metadata

            citations.append(
                CitationSource(
                    document_id=metadata.document_id,
                    source=metadata.source,
                    section=metadata.section_title,
                    page_start=metadata.page_start,
                    page_end=metadata.page_end,
                )
            )

        return citations
