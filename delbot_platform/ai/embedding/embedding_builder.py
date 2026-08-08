from __future__ import annotations

from delbot_platform.ai.embedding.embedding_request import (
    EmbeddingRequest,
)
from delbot_platform.document_intelligence.indexer.indexed_document import (
    IndexedDocument,
)
from delbot_platform.document_intelligence.models.semantic_chunk import (
    SemanticChunk,
)


class EmbeddingBuilder:
    """
    Convert IndexedDocument into EmbeddingRequest objects.
    """

    def build(
        self,
        document: IndexedDocument,
    ) -> list[EmbeddingRequest]:

        requests: list[EmbeddingRequest] = []

        collection = document.index

        for index, chunk in enumerate(
            collection,
            start=1,
        ):
            requests.append(
                self._build_request(
                    index=index,
                    chunk=chunk,
                )
            )

        return requests

    def _build_request(
        self,
        *,
        index: int,
        chunk: SemanticChunk,
    ) -> EmbeddingRequest:

        return EmbeddingRequest(
            id=f"chunk-{index:06d}",
            text=chunk.text,
            metadata={
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "paragraph_count": len(
                    chunk.paragraphs,
                ),
            },
        )
