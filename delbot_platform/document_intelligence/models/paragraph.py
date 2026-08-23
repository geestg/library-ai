from __future__ import annotations

from dataclasses import dataclass

from delbot_platform.document_intelligence.models.heading import (
    Heading,
)


@dataclass(slots=True, frozen=True)
class Paragraph:
    """
    Represents a semantic paragraph extracted from a document.
    """

    text: str

    page_number: int

    heading: Heading | None = None
