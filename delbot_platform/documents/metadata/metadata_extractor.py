from __future__ import annotations

import re

from delbot_platform.documents.metadata.document_metadata import (
    DocumentMetadata,
)


class MetadataExtractor:
    """
    Canonical metadata extractor.

    Source of truth:
        document_metadata.DocumentMetadata

    Current responsibility:
        - title
        - authors
        - year
        - language

    Future PR:
        - institution
        - study program
        - abstract
        - keywords
        - degree
        - toc
    """

    _YEAR_PATTERN = re.compile(r"\b(19\d{2}|20\d{2})\b")

    def extract(
        self,
        *,
        document_id: str,
        pages: list[str],
    ) -> DocumentMetadata:

        metadata = DocumentMetadata(
            document_id=document_id,
            source="repository",
            pages=len(pages),
            blocks=0,
            sections=0,
            chunks=0,
        )

        metadata.language = self._detect_language(pages)

        metadata.title = self._extract_title(pages)

        metadata.authors = self._extract_authors(pages)

        metadata.year = self._extract_year(pages)

        return metadata

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------

    def _extract_title(
        self,
        pages: list[str],
    ) -> str | None:

        for page in pages[:2]:

            for line in page.splitlines():

                line = line.strip()

                if len(line) < 10:
                    continue

                upper = line.upper()

                if upper.startswith("BAB "):
                    continue

                if "PROGRAM STUDI" in upper:
                    continue

                if "FAKULTAS" in upper:
                    continue

                if "INSTITUT" in upper:
                    continue

                if "UNIVERSITAS" in upper:
                    continue

                if "TUGAS AKHIR" in upper:
                    continue

                if "SKRIPSI" in upper:
                    continue

                return line

        return None

    # ---------------------------------------------------------
    # Author
    # ---------------------------------------------------------

    def _extract_authors(
        self,
        pages: list[str],
    ) -> list[str]:

        # Placeholder.
        # Akan diganti memakai classifier AUTHOR.
        return []

    # ---------------------------------------------------------
    # Year
    # ---------------------------------------------------------

    def _extract_year(
        self,
        pages: list[str],
    ) -> int | None:

        for page in pages[:3]:

            match = self._YEAR_PATTERN.search(page)

            if match:

                year = int(match.group())

                if 1990 <= year <= 2100:

                    return year

        return None

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    def _detect_language(
        self,
        pages: list[str],
    ) -> str:

        sample = "\n".join(
            pages[:2]
        ).lower()

        indonesia = (
            "abstrak",
            "bab",
            "pendahuluan",
            "kesimpulan",
            "daftar",
            "penelitian",
        )

        english = (
            "abstract",
            "chapter",
            "introduction",
            "conclusion",
            "references",
        )

        id_score = sum(
            word in sample
            for word in indonesia
        )

        en_score = sum(
            word in sample
            for word in english
        )

        if en_score > id_score:
            return "en"

        return "id"
