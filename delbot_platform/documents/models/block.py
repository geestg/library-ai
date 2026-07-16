from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Block:

    id: str

    page: int

    bbox: tuple[
        float,
        float,
        float,
        float,
    ]

    text: str

    block_type: str

    font_size: float = 0.0

    font_name: str = ""

    bold: bool = False