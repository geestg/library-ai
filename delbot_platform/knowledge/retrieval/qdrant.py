from __future__ import annotations

from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)
from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)
from delbot_platform.knowledge.retrieval.base import (
    Retriever,
)
from delbot_platform.knowledge.retrieval.result import (
    RetrievalResult,
)
from delbot_platform.knowledge.vector.repository.qdrant import (
    QdrantRepository,
)


class QdrantRetriever(
    Retriever,
):

    def __init__(
        self,
    ) -> None:

        self.repository = QdrantRepository()

        self.embedding = EmbeddingPipeline(
            provider="gateway",
        )

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:

        query_chunk = DocumentChunk(
            id="query",
            document_id="query",
            text=query,
            page_start=0,
            page_end=0,
            metadata=ChunkMetadata(
                document_id="query",
                source="query",
                section="query",
                level=0,
                page_start=0,
                page_end=0,
            ),
        )

        vectors = await self.embedding.run(
            [
                query_chunk,
            ],
        )

        results = await self.repository.search(
            vector=vectors[0].vector,
            limit=limit,
        )

        retrieved: list[RetrievalResult] = []

        for item in results:

            payload = item.metadata

            metadata = ChunkMetadata(
                document_id=payload.get(
                    "document_id",
                    "",
                ),
                source=payload.get(
                    "source",
                    "",
                ),
                section=payload.get(
                    "section",
                    "",
                ),
                level=0,
                page_start=payload.get(
                    "page_start",
                    0,
                ),
                page_end=payload.get(
                    "page_end",
                    0,
                ),
            )

            retrieved.append(
                RetrievalResult(
                    id=item.id,
                    score=0.0,
                    content=payload.get(
                        "text",
                        "",
                    ),
                    metadata=metadata,
                )
            )

        return retrieved
