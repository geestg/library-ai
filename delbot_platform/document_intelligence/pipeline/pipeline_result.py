from __future__ import annotations

from dataclasses import dataclass

from ..indexer.indexed_document import IndexedDocument


@dataclass(slots=True)
class PipelineResult:
    source_document: str
    indexed_document: IndexedDocument
    success: bool
