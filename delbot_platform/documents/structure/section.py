from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.block import (
    Block,
)


@dataclass(slots=True)
class Section:

    title: str

    level: int = 0

    blocks: list[Block] = field(
        default_factory=list,
    )

    children: list["Section"] = field(
        default_factory=list,
    )