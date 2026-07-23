from __future__ import annotations

import re

from delbot_platform.document_intelligence.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from delbot_platform.document_intelligence.analyzer.layout_statistics_analyzer import (
    LayoutStatisticsAnalyzer,
)
from delbot_platform.document_intelligence.models.heading import (
    Heading,
)
from delbot_platform.document_intelligence.models.heading_collection import (
    HeadingCollection,
)
from delbot_platform.document_intelligence.models.heading_level import (
    HeadingLevel,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)


class HeadingDetector(DocumentAnalyzer):
    """
    Stage 53

    Detect heading candidates using simple heuristics.

    Output:
        document.metadata["heading_collection"]
    """

    _FORM_FIELDS = {
        "nama",
        "nim",
        "tanggal",
        "tempat",
        "tanda tangan",
        "program studi",
        "fakultas",
        "oleh",
    }

    _HEADING_PATTERNS = (
        re.compile(r"^BAB\s+[IVXLCDM]+$", re.IGNORECASE),
        re.compile(r"^\d+(\.\d+)*\.?$"),
        re.compile(r"^\d+(\.\d+)*\s+.+$"),
        re.compile(r"^LAMPIRAN(\s+[A-Z0-9]+)?$", re.IGNORECASE),
        re.compile(r"^DAFTAR\s+ISI$", re.IGNORECASE),
        re.compile(r"^DAFTAR\s+GAMBAR$", re.IGNORECASE),
        re.compile(r"^DAFTAR\s+TABEL$", re.IGNORECASE),
        re.compile(r"^ABSTRAK$", re.IGNORECASE),
        re.compile(r"^ABSTRACT$", re.IGNORECASE),
        re.compile(r"^KATA\s+PENGANTAR$", re.IGNORECASE),
        re.compile(r"^KESIMPULAN$", re.IGNORECASE),
        re.compile(r"^PENDAHULUAN$", re.IGNORECASE),
        re.compile(r"^TINJAUAN\s+PUSTAKA$", re.IGNORECASE),
        re.compile(r"^METODOLOGI.*$", re.IGNORECASE),
        re.compile(r"^HASIL.*$", re.IGNORECASE),
        re.compile(r"^PEMBAHASAN.*$", re.IGNORECASE),
    )

    def analyze(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        statistics = LayoutStatisticsAnalyzer().analyze(
            document,
        )

        median_font = statistics.median_font_size

        collection = HeadingCollection()

        for page in document.pages:

            for block in page.blocks:

                for line in block.lines:

                    text = self._line_text(
                        line,
                    )

                    if not text:
                        continue

                    if not self._is_heading_candidate(
                        text=text,
                        line=line,
                        median_font=median_font,
                    ):
                        continue

                    collection.add(
                        Heading(
                            text=text,
                            level=HeadingLevel.UNKNOWN,
                            page_number=page.page_number,
                        )
                    )

        document.metadata["heading_collection"] = collection

        return document

    def _line_text(
        self,
        line,
    ) -> str:
        return "".join(
            span.text
            for span in line.spans
        ).strip()

    def _largest_font(
        self,
        line,
    ) -> float:
        if not line.spans:
            return 0.0

        return max(
            span.font_size
            for span in line.spans
        )

    def _is_bold(
        self,
        line,
    ) -> bool:

        for span in line.spans:

            if span.is_bold:
                return True

            if "bold" in span.font_name.lower():
                return True

        return False

    def _is_form_field(
        self,
        text: str,
    ) -> bool:

        lowered = text.lower().strip()

        if lowered in self._FORM_FIELDS:
            return True

        if lowered.startswith(":"):
            return True

        return False

    def _looks_like_number(
        self,
        text: str,
    ) -> bool:

        return bool(
            re.fullmatch(
                r"[0-9A-Za-z./-]+",
                text,
            )
        )

    def _matches_heading_pattern(
        self,
        text: str,
    ) -> bool:

        for pattern in self._HEADING_PATTERNS:
            if pattern.match(text):
                return True

        return False

    def _is_all_caps(
        self,
        text: str,
    ) -> bool:

        letters = [
            c
            for c in text
            if c.isalpha()
        ]

        if not letters:
            return False

        upper = sum(
            c.isupper()
            for c in letters
        )

        return (upper / len(letters)) >= 0.9

    def _is_heading_candidate(
        self,
        *,
        text: str,
        line,
        median_font: float,
    ) -> bool:

        if len(text) > 80:
            return False

        if len(text.split()) > 12:
            return False

        if text.endswith("."):
            return False

        if self._is_form_field(text):
            return False

        if self._looks_like_number(text):
            return False

        if self._matches_heading_pattern(text):
            return True

        largest_font = self._largest_font(
            line,
        )

        bold = self._is_bold(
            line,
        )

        all_caps = self._is_all_caps(
            text,
        )

        score = 0

        if largest_font > median_font:
            score += 1

        if bold:
            score += 1

        if all_caps:
            score += 1

        return score >= 2