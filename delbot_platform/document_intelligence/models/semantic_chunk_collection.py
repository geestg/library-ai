from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.semantic_chunk import (
    SemanticChunk,
)


@dataclass(slots=True)
class SemanticChunkCollection:

    chunks: list[SemanticChunk] = field(
        default_factory=list,
    )

    def __iter__(
        self,
    ):
        return iter(
            self.chunks,
        )

    def __len__(
        self,
    ) -> int:
        return len(
            self.chunks,
        )

    def add(
        self,
        chunk: SemanticChunk,
    ) -> None:
        self.chunks.append(
            chunk,
        )
