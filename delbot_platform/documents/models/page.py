from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.block import (
    Block,
)


@dataclass(slots=True, frozen=True)
class Page:

    number: int

    width: float

    height: float

    blocks: list[Block] = field(
        default_factory=list,
    )