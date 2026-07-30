from __future__ import annotations

from dataclasses import dataclass, field

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)


@dataclass(slots=True)
class DocumentChunk:
    """
    Canonical semantic chunk.

    This object is the single chunk model flowing through the
    indexing pipeline.

    Pipeline

        SectionBuilder
                ↓
        ChunkBuilder
                ↓
        DocumentChunk
                ↓
        ChunkMetadataBuilder
                ↓
        EmbeddingPipeline
                ↓
        VectorStore

    The embedding pipeline should never depend directly on
    section objects.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    document_id: str
    chunk_id: str

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    page_start: int
    page_end: int

    section_title: str | None = None
    chapter: str | None = None

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------

    text: str = ""

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: ChunkMetadata | None = None

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    embedding: list[float] | None = field(
        default=None,
        repr=False,
    )

    score: float | None = field(
        default=None,
        repr=False,
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def character_count(self) -> int:
        return len(self.text)

    def has_embedding(self) -> bool:
        return self.embedding is not None

    def attach_metadata(
        self,
        metadata: ChunkMetadata,
    ) -> None:
        self.metadata = metadata

    def attach_embedding(
        self,
        embedding: list[float],
    ) -> None:
        self.embedding = embedding
