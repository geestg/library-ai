from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CitationSource:

    document_id: str

    source: str

    section: str

    page_start: int | None = None

    page_end: int | None = None