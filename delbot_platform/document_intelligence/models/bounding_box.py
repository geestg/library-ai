from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BoundingBox:

    left: float

    top: float

    right: float

    bottom: float
