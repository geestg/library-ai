from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from delbot_platform.document_intelligence.models.page import (
    Page,
)


@dataclass(slots=True)
class ParsedDocument:

    title: str

    file_path: str

    pages: list[Page] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
