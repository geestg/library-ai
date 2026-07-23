from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.document_intelligence.models.heading import (
    Heading,
)


@dataclass(slots=True)
class HeadingCollection:
    """
    Collection of semantic headings.
    """

    headings: list[Heading] = field(
        default_factory=list,
    )

    def __iter__(self):
        return iter(self.headings)

    def __len__(self):
        return len(self.headings)

    def add(
        self,
        heading: Heading,
    ) -> None:
        self.headings.append(
            heading,
        )
