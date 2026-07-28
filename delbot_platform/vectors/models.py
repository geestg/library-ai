from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class VectorRecord:
    """
    Canonical vector representation used across the DELBot
    embedding, vector storage, retrieval, and reranking pipeline.
    """

    id: str

    score: float = 0.0

    vector: list[float] | None = None

    metadata: dict[str, Any] | None = None
