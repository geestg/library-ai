from __future__ import annotations

from delbot_platform.knowledge.models import DocumentChunk
from delbot_platform.research.models import Citation


class CitationBuilder:

    def build(
        self,
        results: list[DocumentChunk],
    ) -> list[Citation]:

        citations: list[Citation] = []

        for chunk in results:

            citations.append(
                Citation(
                    document=chunk.document,
                    page=chunk.page,
                    chunk_id=chunk.chunk_id,
                    score=chunk.rerank_score,
                    text=chunk.text,
                    metadata=chunk.metadata,
                )
            )

        return citations

    