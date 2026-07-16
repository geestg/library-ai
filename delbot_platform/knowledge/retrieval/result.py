from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalResult:

    id: str

    score: float

    content: str

    metadata: dict