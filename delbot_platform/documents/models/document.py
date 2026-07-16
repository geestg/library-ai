from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.metadata import (
    Metadata,
)
from delbot_platform.documents.models.page import (
    Page,
)


@dataclass(slots=True, frozen=True)
class Document:

    id: str

    title: str

    source: str

    language: str

    pages: list[Page] = field(
        default_factory=list,
    )

    metadata: Metadata = field(
        default_factory=Metadata,
    )