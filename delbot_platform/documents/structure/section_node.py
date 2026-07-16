from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.block import Block


@dataclass(slots=True)
class SectionNode:

    title: str

    level: int

    blocks: list[Block] = field(
        default_factory=list,
    )

    children: list["SectionNode"] = field(
        default_factory=list,
    )