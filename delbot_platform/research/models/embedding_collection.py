from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.research.models.embedding import (
    Embedding,
)


@dataclass(slots=True)
class EmbeddingCollection:

    embeddings: list[Embedding] = field(
        default_factory=list,
    )

    def __iter__(
        self,
    ):
        return iter(
            self.embeddings,
        )

    def __len__(
        self,
    ) -> int:
        return len(
            self.embeddings,
        )

    def add(
        self,
        embedding: Embedding,
    ) -> None:

        self.embeddings.append(
            embedding,
        )
