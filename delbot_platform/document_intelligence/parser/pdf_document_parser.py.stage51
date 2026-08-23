from __future__ import annotations

from delbot_platform.document_intelligence.loader.loaded_document import (
    LoadedDocument,
)
from delbot_platform.document_intelligence.mapper.layout_mapper import (
    LayoutMapper,
)
from delbot_platform.document_intelligence.mapper.pymupdf_mapper import (
    PyMuPDFMapper,
)
from delbot_platform.document_intelligence.models.page import (
    Page,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.document_intelligence.parser.document_parser import (
    DocumentParser,
)


class PDFDocumentParser(DocumentParser):

    def __init__(
        self,
        mapper: LayoutMapper | None = None,
    ) -> None:
        self._mapper = mapper or PyMuPDFMapper()

    def _build_pages(
        self,
        document: LoadedDocument,
    ) -> list[Page]:

        backend = document.backend_document

        pages: list[Page] = []

        for page_index, pdf_page in enumerate(backend):

            pages.append(
                self._mapper.build_page(
                    page_index=page_index,
                    page=pdf_page,
                ),
            )

        return pages

    def parse(
        self,
        document: LoadedDocument,
    ) -> ParsedDocument:

        pages = self._build_pages(document)

        backend = document.backend_document

        return ParsedDocument(
            title=document.source_path.stem,
            file_path=str(document.source_path),
            pages=pages,
            metadata={
                "page_count": backend.page_count,
            },
        )
