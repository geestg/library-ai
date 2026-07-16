from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DocumentIndexResult:

    document_id: str

    source: str

    pages: int

    blocks: int

    sections: int

    chunks: int

    vectors: int

    elapsed: float

    success: bool = True