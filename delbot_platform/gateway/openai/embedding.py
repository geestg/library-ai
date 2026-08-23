from __future__ import annotations

import time

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class EmbeddingData:

    index: int

    embedding: list[float]

    object: str = "embedding"


@dataclass(slots=True)
class EmbeddingResponse:

    model: str

    data: list[EmbeddingData]

    id: str = "emb-delbot"

    object: str = "list"

    created: int = field(
        default_factory=lambda: int(time.time()),
    )