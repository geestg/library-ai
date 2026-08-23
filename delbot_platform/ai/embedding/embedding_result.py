from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class EmbeddingResult:
    """
    Result returned by an embedding provider.
    """

    id: str

    vector: list[float]

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
