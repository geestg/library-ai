from __future__ import annotations

import re

from delbot_platform.document_intelligence.models.block import (
    Block,
)
from delbot_platform.document_intelligence.models.paragraph import (
    Paragraph,
)
from delbot_platform.document_intelligence.models.paragraph_collection import (
    ParagraphCollection,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class ParagraphBuilder:
    """
    Build semantic paragraphs from ParsedDocument.

    MVP Strategy
    ------------

    Block
        ↓
    Normalize
        ↓
    Merge short blocks
        ↓
    ParagraphCollection
    """

    _MIN_WORDS = 12
    _MIN_CHARS = 80

    def build(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        collection = ParagraphCollection()

        pending_text = ""
        pending_page = 0

        for page in document.pages:

            for block in page.blocks:

                text = self._build_paragraph_text(
                    block,
                )

                text = self._normalize_text(
                    text,
                )

                if not text:
                    continue

                if not pending_text:

                    pending_text = text
                    pending_page = page.page_number
                    continue

                if self._should_merge(
                    pending_text,
                    text,
                    pending_page,
                    page.page_number,
                ):

                    pending_text = (
                        pending_text
                        + " "
                        + text
                    )

                    continue

                collection.add(
                    Paragraph(
                        text=pending_text,
                        page_number=pending_page,
                        heading=None,
                    )
                )

                pending_text = text
                pending_page = page.page_number

        if pending_text:

            collection.add(
                Paragraph(
                    text=pending_text,
                    page_number=pending_page,
                    heading=None,
                )
            )

        document.metadata[
            "paragraph_collection"
        ] = collection

        return document

    def _build_paragraph_text(
        self,
        block: Block,
    ) -> str:

        lines: list[str] = []

        for line in block.lines:

            text = "".join(
                span.text
                for span in line.spans
            )

            text = self._normalize_text(
                text,
            )

            if text:
                lines.append(
                    text,
                )

        return " ".join(
            lines,
        )

    def _normalize_text(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def _should_merge(
        self,
        current: str,
        next_text: str,
        current_page: int,
        next_page: int,
    ) -> bool:

        if current_page != next_page:
            return False

        if self._looks_like_heading(
            next_text,
        ):
            return False

        if (
            len(current) < self._MIN_CHARS
            or len(current.split()) < self._MIN_WORDS
        ):
            return True

        return False

    def _looks_like_heading(
        self,
        text: str,
    ) -> bool:

        upper = text.upper()

        if upper.startswith("BAB "):
            return True

        if re.match(
            r"^\d+(\.\d+)*",
            text,
        ):
            return True

        if text.isupper():
            return True

        return False
