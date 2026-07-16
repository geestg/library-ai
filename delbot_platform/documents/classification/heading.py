from __future__ import annotations

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)

from delbot_platform.documents.models.block import (
    Block,
)


class HeadingClassifier:
    """
    Classify a Block into a semantic document type.

    This classifier updates the Block in-place and also
    returns the resolved DocumentBlockType.
    """

    def classify(
        self,
        block: Block,
    ) -> DocumentBlockType:

        text = block.text.strip()

        if not text:

            block.type = DocumentBlockType.UNKNOWN
            return block.type

        if self._is_date(text):

            block.type = DocumentBlockType.DATE
            return block.type

        if self._is_institution(text):

            block.type = DocumentBlockType.INSTITUTION
            return block.type

        if self._is_title(block):

            block.type = DocumentBlockType.TITLE
            return block.type

        if self._looks_like_author(block):

            block.type = DocumentBlockType.AUTHOR
            return block.type

        if self._is_heading(block):

            block.type = DocumentBlockType.HEADING
            return block.type

        block.type = DocumentBlockType.PARAGRAPH

        return block.type

    def classify_all(
        self,
        blocks: list[Block],
    ) -> list[Block]:

        for block in blocks:

            self.classify(
                block,
            )

        return blocks

    def _is_date(
        self,
        text: str,
    ) -> bool:

        months = (

            "JANUARI",
            "FEBRUARI",
            "MARET",
            "APRIL",
            "MEI",
            "JUNI",
            "JULI",
            "AGUSTUS",
            "SEPTEMBER",
            "OKTOBER",
            "NOVEMBER",
            "DESEMBER",

        )

        upper = text.upper()

        return any(
            month in upper
            for month in months
        )

    def _is_institution(
        self,
        text: str,
    ) -> bool:

        keywords = (

            "INSTITUT",
            "UNIVERSITAS",
            "FAKULTAS",
            "PROGRAM STUDI",

        )

        upper = text.upper()

        return any(
            keyword in upper
            for keyword in keywords
        )

    def _is_title(
        self,
        block: Block,
    ) -> bool:

        return (

            block.page == 1

            and block.font_size >= 14

            and block.bold

        )

    def _looks_like_author(
        self,
        block: Block,
    ) -> bool:

        text = block.text.strip()

        if len(text.split()) > 4:

            return False

        if any(
            c.isdigit()
            for c in text
        ):

            return False

        return (

            block.page == 1

            and block.bold

            and block.font_size >= 12

        )

    def _is_heading(
        self,
        block: Block,
    ) -> bool:

        return (

            block.font_size >= 13

            and block.bold

        )