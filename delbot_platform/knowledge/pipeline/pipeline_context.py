from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgePipelineContext:

    document_id: str

    source: str

    chunk_count: int

    vector_count: int
