from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ChunkMetadata:
    """
    Canonical metadata describing one semantic chunk.

    Every chunk indexed into the vector database should carry
    this metadata.

    Future PRs may extend this model without breaking the API.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    document_id: str
    chunk_id: str

    # ---------------------------------------------------------
    # Source
    # ---------------------------------------------------------

    source: str = "repository"

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    page_start: int = 0
    page_end: int = 0

    section_title: str | None = None
    chapter: str | None = None

    # ---------------------------------------------------------
    # Hierarchy
    # ---------------------------------------------------------

    level: int = 0

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    token_count: int = 0
    character_count: int = 0

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    language: str = "id"

    # ---------------------------------------------------------
    # Optional metadata
    # ---------------------------------------------------------

    tags: list[str] = field(default_factory=list)

    keywords: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Future
    # ---------------------------------------------------------

    embedding_model: str | None = None

    embedding_version: str | None = None

    checksum: str | None = None
