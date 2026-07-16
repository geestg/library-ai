from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RerankResult:

    id: str

    score: float

    content: str

    metadata: dict