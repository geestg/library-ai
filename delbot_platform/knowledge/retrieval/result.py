from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)


@dataclass(slots=True)
class RetrievalResult:

    id: str

    score: float

    content: str

    metadata: ChunkMetadata
