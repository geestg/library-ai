from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.models.block import (
    Block,
)


@dataclass(slots=True)
class DocumentSection:
    """
    Logical document section.

    A section is the bridge between layout analysis
    and semantic chunk generation.

    Example

        BAB I
            Pendahuluan

        BAB II
            Landasan Teori

    Every section already carries all metadata
    required by downstream pipelines.
    """

    #
    # Identity
    #

    document_id: str

    source: str

    #
    # Structure
    #

    title: str

    chapter: str | None = None

    level: int = 1

    #
    # Location
    #

    page_start: int = 1

    page_end: int = 1

    #
    # Content
    #

    blocks: list[Block] = field(
        default_factory=list,
    )

    text: str = ""

    #
    # Helpers
    #

    def add_block(
        self,
        block: Block,
    ) -> None:

        self.blocks.append(
            block,
        )

        if self.text:

            self.text += "\n"

        self.text += block.text

        self.page_end = max(
            self.page_end,
            block.page,
        )

    def clear(
        self,
    ) -> None:

        self.blocks.clear()

        self.text = ""

    @property
    def block_count(
        self,
    ) -> int:

        return len(
            self.blocks,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self.text,
        )

    def __bool__(
        self,
    ) -> bool:

        return bool(
            self.text.strip(),
        )