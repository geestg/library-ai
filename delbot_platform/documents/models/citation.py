from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Citation:

    document_id: str

    page: int

    heading: str

    chunk_id: str