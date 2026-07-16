from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChunkMetadata:

    document_id: str

    source: str

    section: str

    level: int

    page_start: int | None = None

    page_end: int | None = None

    chapter: str | None = None

    chunk_index: int = 0