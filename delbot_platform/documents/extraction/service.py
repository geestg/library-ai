from __future__ import annotations

from delbot_platform.documents.extraction.block import (
    BlockExtractor,
)

from delbot_platform.documents.loader.sources.local import (
    LocalDocumentSource,
)

from delbot_platform.documents.models.block import (
    Block,
)

from delbot_platform.documents.parser.backend.pymupdf import (
    PyMuPDFBackend,
)


class DocumentExtractionService:
    """
    Extract layout blocks from a PDF document.

    Flow:

        LocalDocumentSource
                │
                ▼
          PyMuPDFBackend
                │
                ▼
              Page
                │
                ▼
         BlockExtractor
                │
                ▼
             Block[]
    """

    def __init__(
        self,
    ) -> None:

        self.backend = PyMuPDFBackend()

        self.extractor = BlockExtractor()

    def extract(
        self,
        pdf_path: str,
    ) -> list[Block]:

        source = LocalDocumentSource(
            pdf_path,
        )

        self.backend.open(
            source,
        )

        blocks: list[Block] = []

        try:

            page_count = self.backend.page_count()

            for index in range(
                page_count,
            ):

                page = self.backend.page(
                    index,
                )

                page_blocks = self.extractor.extract(
                    page,
                )

                blocks.extend(
                    page_blocks,
                )

        finally:

            self.backend.close()

        return blocks