from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.heading import (
    Heading,
)
from delbot_platform.document_intelligence.models.paragraph import (
    Paragraph,
)


@dataclass(slots=True)
class SemanticChunk:
    """
    Represents one semantic chunk that will later be embedded
    and indexed into the vector database.
    """

    text: str

    page_start: int

    page_end: int

    paragraphs: list[Paragraph] = field(
        default_factory=list,
    )

    heading: Heading | None = None

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def paragraph_count(
        self,
    ) -> int:
        return len(
            self.paragraphs,
        )

    @property
    def character_count(
        self,
    ) -> int:
        return len(
            self.text,
        )

    @property
    def word_count(
        self,
    ) -> int:
        return len(
            self.text.split(),
        )
