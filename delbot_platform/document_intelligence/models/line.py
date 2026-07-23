from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.span import (
    Span,
)


@dataclass(slots=True)
class Line:

    spans: list[Span] = field(
        default_factory=list,
    )
