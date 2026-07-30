from __future__ import annotations

import re

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

    _TITLE_KEYWORDS = {
        "ANALISIS",
        "PERANCANGAN",
        "IMPLEMENTASI",
        "PENGEMBANGAN",
        "DESAIN",
        "RANCANG",
        "SISTEM",
        "KLASIFIKASI",
        "PREDIKSI",
        "OPTIMASI",
        "PEMANFAATAN",
    }

    _TITLE_BLACKLIST = {
        "TUGAS AKHIR",
        "TUGASAKHIR",
        "SKRIPSI",
        "TESIS",
        "DOKUMEN TUGAS AKHIR",
        "HALAMAN JUDUL",
        "HALAMAN PENGESAHAN",
        "LEMBAR PENGESAHAN",
        "ABSTRAK",
        "ABSTRACT",
        "KATA PENGANTAR",
        "PRAKATA",
        "DAFTAR ISI",
        "DAFTAR GAMBAR",
        "DAFTAR TABEL",
        "OLEH",
    }

    _TITLE_REJECT = (
        "DIAJUKAN",
        "DISAMPAIKAN",
        "SEBAGAI SALAH SATU SYARAT",
        "UNTUK MEMPEROLEH",
        "PROGRAM STUDI",
        "FAKULTAS",
        "INSTITUT",
        "UNIVERSITAS",
    )

    _TITLE_THRESHOLD = 5

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
            self.classify(block)

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

        return any(month in upper for month in months)

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

        return any(keyword in upper for keyword in keywords)

    def _is_title(
        self,
        block: Block,
    ) -> bool:

        text = block.text.strip()

        if not text:
            return False

        upper = text.upper()

        if upper in self._TITLE_BLACKLIST:
            return False

        for phrase in self._TITLE_REJECT:
            if phrase in upper:
                return False

        words = text.split()

        if len(words) < 3:
            return False

        if len(words) > 30:
            return False

        score = 0

        if block.page == 1:
            score += 2

        if block.bold:
            score += 2

        if block.font_size >= 14:
            score += 2

        if any(keyword in upper for keyword in self._TITLE_KEYWORDS):
            score += 2

        if any(ch.isdigit() for ch in text):
            score -= 2

        if upper.endswith(":"):
            score -= 1

        if len(words) >= 8:
            score += 1

        return score >= self._TITLE_THRESHOLD

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

        text = block.text.strip()

        if not text:
            return False

        upper = text.upper()

        reject_exact = {
            "ABSTRAK",
            "ABSTRACT",
            "DAFTAR ISI",
            "DAFTAR TABEL",
            "DAFTAR GAMBAR",
            "DAFTAR LAMPIRAN",
            "TUGAS AKHIR",
            "TUGASAKHIR",
            "SKRIPSI",
            "TESIS",
            "PRAKATA",
            "KATA PENGANTAR",
            "KATA PENGHANTAR",
            "UCAPAN TERIMA KASIH",
            "UCAPAN TERIMAKASIH",
            "HALAMAN PENGESAHAN",
            "LEMBAR PENGESAHAN",
            "OLEH",
        }

        if upper in reject_exact:
            return False

        reject_contains = (
            "PROGRAM STUDI",
            "FAKULTAS",
            "UNIVERSITAS",
            "INSTITUT",
            "DIAJUKAN",
            "SEBAGAI SALAH SATU SYARAT",
            "NIM",
            "PERNYATAAN",
            "PERSETUJUAN",
        )

        if any(k in upper for k in reject_contains):
            return False

        if any(ch.isdigit() for ch in text):

            if not (
                upper.startswith("BAB")
                or re.match(r"^[0-9]+(\.[0-9]+)*", text)
            ):
                return False

        heading_keywords = (
            "BAB",
            "PENDAHULUAN",
            "TINJAUAN PUSTAKA",
            "METODOLOGI",
            "METODE",
            "HASIL",
            "PEMBAHASAN",
            "KESIMPULAN",
            "SARAN",
            "LAMPIRAN",
            "DAFTAR PUSTAKA",
        )

        numbered = (
            re.match(r"^[0-9]+(\.[0-9]+)*", text)
            or re.match(r"^[A-Z]\.", text)
        )

        return (
            block.bold
            and block.font_size >= 13
            and (
                any(k in upper for k in heading_keywords)
                or numbered
            )
        )

