from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VectorRecord:

    id: str

    vector: list[float]

    metadata: dict