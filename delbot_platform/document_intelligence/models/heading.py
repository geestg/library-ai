from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.document_intelligence.models.heading_level import (
    HeadingLevel,
)


@dataclass(slots=True, frozen=True)
class Heading:
    """
    Represents a semantic heading inside a document.

    This model intentionally stores only semantic information.
    Layout-specific metadata remains inside parser artifacts.
    """

    text: str

    level: HeadingLevel

    page_number: int
