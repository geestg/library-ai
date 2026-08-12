from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IndexedDocument:
    source_document: object
    index: object
    metadata: dict
