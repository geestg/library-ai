from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class ChunkMetadata:
    """
    Canonical metadata attached to every semantic chunk.

    This object is propagated throughout the indexing,
    retrieval, reranking, citation, and RAG pipeline.
    """

    document_id: str

    source: str

    section: str

    level: int

    page_start: int

    page_end: int

    chapter: str | None = None

    chunk_index: int = 0

    total_chunks: int = 0

    language: str = "id"

    repository_id: str | None = None

    heading: str | None = None

    attributes: dict[str, str] = field(
        default_factory=dict,
    )