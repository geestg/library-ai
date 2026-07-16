from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Chunk:

    id: str

    page_start: int

    page_end: int

    heading: str

    content: str