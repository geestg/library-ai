from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.document_intelligence.models.bounding_box import (
    BoundingBox,
)


@dataclass(slots=True)
class Span:

    text: str

    font_name: str

    font_size: float

    is_bold: bool = False

    is_italic: bool = False

    bbox: BoundingBox | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
