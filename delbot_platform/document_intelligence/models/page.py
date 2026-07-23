from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.document_intelligence.models.block import (
    Block,
)


@dataclass(slots=True)
class Page:

    page_index: int

    page_number: int

    text: str = ""

    blocks: list[Block] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
