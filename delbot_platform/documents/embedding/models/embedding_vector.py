from __future__ import annotations

from dataclasses import dataclass, field

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)
from delbot_platform.documents.metadata.mapper.chunk_metadata_mapper import (
    ChunkMetadataMapper,
)


@dataclass(slots=True)
class EmbeddingVector:
    """
    Canonical embedding object.

    This is the only embedding representation produced by the
    document indexing pipeline.

    Pipeline

        DocumentChunk
                │
                ▼
        EmbeddingProvider
                │
                ▼
        EmbeddingVector
                │
                ▼
        Vector Repository
                │
                ▼
             Qdrant
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    document_id: str
    chunk_id: str

    # ---------------------------------------------------------
    # Source Content
    # ---------------------------------------------------------

    text: str

    # ---------------------------------------------------------
    # Vector
    # ---------------------------------------------------------

    vector: list[float]

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: ChunkMetadata

    # ---------------------------------------------------------
    # Provider Information
    # ---------------------------------------------------------

    provider: str = "local"

    model: str = ""

    dimension: int = 0

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    created_at: float | None = None

    extra: dict[str, object] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @property
    def has_vector(
        self,
    ) -> bool:

        return bool(self.vector)

    @property
    def size(
        self,
    ) -> int:

        return len(self.vector)
