from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.line import (
    Line,
)


@dataclass(slots=True)
class Block:

    lines: list[Line] = field(
        default_factory=list,
    )
