from __future__ import annotations

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)
from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)
from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)
from delbot_platform.documents.metadata.mapper.chunk_metadata_mapper import (
    ChunkMetadataMapper,
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

        self.repository = None

        self.embedding = None


    def _initialize(
        self,
    ) -> None:

        if self.repository is None:
            self.repository = QdrantRepository()

        if self.embedding is None:
            self.embedding = EmbeddingPipeline(
                provider="gateway",
            )

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:

        self._initialize()

        query_chunk = DocumentChunk(
            document_id="query",
            chunk_id="query",
            page_start=0,
            page_end=0,
            section_title="query",
            text=query,
            metadata=ChunkMetadata(
                document_id="query",
                chunk_id="query",
                source="query",
                section_title="query",
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

            metadata = (
                ChunkMetadataMapper.from_payload(payload)
            )

            retrieved.append(
                RetrievalResult(
                    id=item.id,
                    score=item.score,
                    content=payload.get(
                        "text",
                        "",
                    ),
                    metadata=metadata,
                )
            )

        return retrieved
