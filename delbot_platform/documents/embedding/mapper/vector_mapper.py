from __future__ import annotations

from delbot_platform.documents.embedding.models import (
    EmbeddingVector,
)
from delbot_platform.documents.metadata.mapper.chunk_metadata_mapper import (
    ChunkMetadataMapper,
)
from delbot_platform.vectors import (
    VectorRecord,
)


class EmbeddingVectorMapper:
    """
    Maps document-domain EmbeddingVector objects into
    storage-domain VectorRecord objects.
    """

    @staticmethod
    def to_vector_record(
        embedding: EmbeddingVector,
    ) -> VectorRecord:

        metadata = (
            ChunkMetadataMapper.to_payload(
                embedding.metadata,
                document_id=embedding.document_id,
                chunk_id=embedding.chunk_id,
                provider=embedding.provider,
                model=embedding.model,
                dimension=embedding.dimension,
                text=embedding.text,
            )
            if embedding.metadata is not None
            else {}
        )

        return VectorRecord(
            id=embedding.chunk_id,
            vector=embedding.vector,
            metadata=metadata,
        )

    @staticmethod
    def to_vector_records(
        embeddings: list[EmbeddingVector],
    ) -> list[VectorRecord]:

        return [
            EmbeddingVectorMapper.to_vector_record(
                embedding,
            )
            for embedding in embeddings
        ]
