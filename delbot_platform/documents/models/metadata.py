from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True, frozen=True)
class Metadata:

    title: str = ""

    author: str = ""

    year: int | None = None

    faculty: str = ""

    program: str = ""

    keywords: list[str] = field(
        default_factory=list,
    )