from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)


@dataclass(slots=True)
class Block:
    """
    Atomic layout element extracted from a PDF page.

    Block is the canonical representation shared by
    parser, classifier, section builder and chunk builder.

    Every stage of the document pipeline should exchange
    Block objects instead of raw dictionaries.
    """

    #
    # Identity
    #

    id: str

    #
    # Position
    #

    page: int

    bbox: tuple[
        float,
        float,
        float,
        float,
    ]

    #
    # Content
    #

    text: str

    #
    # Classification
    #

    type: DocumentBlockType = (
        DocumentBlockType.UNKNOWN
    )

    #
    # Typography
    #

    font_size: float = 0.0

    font_name: str = ""

    bold: bool = False

    italic: bool = False

    #
    # Confidence
    #

    confidence: float = 1.0

    #
    # Extra attributes
    #

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def block_type(
        self,
    ) -> str:
        """
        Backward compatibility.

        Existing parser code still accesses block_type.
        """

        return self.type.value

    def is_heading(
        self,
    ) -> bool:

        return (
            self.type
            == DocumentBlockType.HEADING
        )

    def is_paragraph(
        self,
    ) -> bool:

        return (
            self.type
            == DocumentBlockType.PARAGRAPH
        )

    def is_title(
        self,
    ) -> bool:

        return (
            self.type
            == DocumentBlockType.TITLE
        )

    def is_empty(
        self,
    ) -> bool:

        return (
            not self.text.strip()
        )