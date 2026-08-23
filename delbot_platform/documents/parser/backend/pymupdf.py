from __future__ import annotations

import fitz

from delbot_platform.documents.loader.source import (
    DocumentSource,
)
from delbot_platform.documents.parser.backend.base import (
    PDFBackend,
)


class PyMuPDFBackend(PDFBackend):

    def __init__(
        self,
    ) -> None:

        self._document: fitz.Document | None = None

    def open(
        self,
        source: DocumentSource,
    ) -> None:

        self.close()

        self._document = fitz.open(
            source.path(),
        )

    def metadata(
        self,
    ) -> dict:

        self._ensure_open()

        return dict(
            self._document.metadata,
        )

    def page_count(
        self,
    ) -> int:

        self._ensure_open()

        return len(
            self._document,
        )

    def page(
        self,
        index: int,
    ):

        self._ensure_open()

        return self._document.load_page(
            index,
        )

    def toc(
        self,
    ) -> list:

        self._ensure_open()

        return self._document.get_toc()

    def close(
        self,
    ) -> None:

        if self._document is not None:

            self._document.close()

            self._document = None

    def _ensure_open(
        self,
    ) -> None:

        if self._document is None:

            raise RuntimeError(
                "PDF backend is not open."
            )