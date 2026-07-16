from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)


@dataclass(slots=True)
class DocumentChunk:
    """
    Canonical semantic chunk used throughout the DELBot
    indexing and retrieval pipeline.

    This is the single source of truth for chunk objects.
    """

    id: str

    document_id: str

    text: str

    page_start: int

    page_end: int

    metadata: ChunkMetadata