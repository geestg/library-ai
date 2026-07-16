from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.structure.section import (
    Section,
)


@dataclass(slots=True)
class DocumentStructure:

    cover: list[Section] = field(
        default_factory=list,
    )

    front_matter: list[Section] = field(
        default_factory=list,
    )

    sections: list[Section] = field(
        default_factory=list,
    )

    references: list[Section] = field(
        default_factory=list,
    )