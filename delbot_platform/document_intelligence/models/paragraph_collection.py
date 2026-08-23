from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.paragraph import (
    Paragraph,
)


@dataclass(slots=True)
class ParagraphCollection:
    """
    Collection of semantic paragraphs.
    """

    paragraphs: list[Paragraph] = field(
        default_factory=list,
    )

    def __iter__(self):
        return iter(self.paragraphs)

    def __len__(self):
        return len(self.paragraphs)

    def add(
        self,
        paragraph: Paragraph,
    ) -> None:
        self.paragraphs.append(
            paragraph,
        )
