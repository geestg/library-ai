from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)


@dataclass(slots=True)
class Citation:

    document: str
    page: int | str
    chunk_id: str
    score: float
    text: str
    metadata: Any = None


class CitationBuilder:

    def build(
        self,
        results: list[DocumentChunk],
    ) -> list[Citation]:

        citations: list[Citation] = []

        for chunk in results:

            metadata = chunk.metadata

            source = None

            if metadata is not None:
                source = getattr(
                    metadata,
                    "source",
                    None,
                )

            if chunk.page_start == chunk.page_end:
                page = chunk.page_start
            else:
                page = f"{chunk.page_start}-{chunk.page_end}"

            citations.append(
                Citation(
                    document=chunk.document_id,
                    page=page,
                    chunk_id=chunk.chunk_id,
                    score=chunk.score or 0.0,
                    text=chunk.text,
                    metadata=source,
                )
            )

        return citations
