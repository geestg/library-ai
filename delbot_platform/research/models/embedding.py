from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class Embedding:
    """
    Represents one embedded semantic chunk.

    The vector is intentionally optional because the object is
    first created by EmbeddingBuilder and later populated by an
    EmbeddingProvider.
    """

    id: str

    text: str

    vector: list[float] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def dimension(
        self,
    ) -> int:
        return len(
            self.vector,
        )

    @property
    def is_embedded(
        self,
    ) -> bool:
        return bool(
            self.vector,
        )
