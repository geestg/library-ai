from __future__ import annotations

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)

from delbot_platform.documents.models.block import (
    Block,
)


class HeadingClassifier:


    def classify(
        self,
        block: Block,
    ) -> DocumentBlockType:

        text = block.text.strip()


        if not text:

            return DocumentBlockType.UNKNOWN


        if self._is_date(
            text,
        ):

            return DocumentBlockType.DATE


        if self._is_institution(
            text,
        ):

            return DocumentBlockType.INSTITUTION


        if self._is_title(
            block,
        ):

            return DocumentBlockType.TITLE


        if self._looks_like_author(
            block,
        ):

            return DocumentBlockType.AUTHOR


        if self._is_heading(
            block,
        ):

            return DocumentBlockType.HEADING


        return DocumentBlockType.PARAGRAPH



    def _is_date(
        self,
        text: str,
    ) -> bool:

        months = [
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
        ]

        upper = text.upper()

        return any(
            month in upper
            for month in months
        )



    def _is_institution(
        self,
        text: str,
    ) -> bool:

        upper = text.upper()


        keywords = [
            "INSTITUT",
            "UNIVERSITAS",
            "FAKULTAS",
            "PROGRAM STUDI",
        ]


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

        words = text.split()


        if len(words) > 4:

            return False


        if any(
            char.isdigit()
            for char in text
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