from __future__ import annotations

from delbot_platform.documents.loader.source import (
    DocumentSource,
)
from delbot_platform.documents.models.document import (
    Document,
)
from delbot_platform.documents.models.metadata import (
    Metadata,
)
from delbot_platform.documents.models.page import (
    Page,
)
from delbot_platform.documents.parser.backend.base import (
    PDFBackend,
)
from delbot_platform.documents.parser.backend.pymupdf import (
    PyMuPDFBackend,
)
from delbot_platform.documents.parser.base import (
    DocumentParser,
)


class PDFParser(DocumentParser):

    def __init__(
        self,
        backend: PDFBackend | None = None,
    ) -> None:

        self.backend = (
            backend
            if backend is not None
            else PyMuPDFBackend()
        )

    def parse(
        self,
        source: DocumentSource,
    ) -> Document:

        if not source.exists():

            raise FileNotFoundError(
                source.path(),
            )

        self.backend.open(
            source,
        )

        try:

            raw_metadata = self.backend.metadata()

            pages: list[Page] = []

            for index in range(
                self.backend.page_count(),
            ):

                pdf_page = self.backend.page(
                    index,
                )

                rect = pdf_page.rect

                pages.append(
                    Page(
                        number=index + 1,
                        width=rect.width,
                        height=rect.height,
                    )
                )

            metadata = Metadata(
                title=raw_metadata.get(
                    "title",
                    "",
                ),
                author=raw_metadata.get(
                    "author",
                    "",
                ),
            )

            title = (
                metadata.title
                or source.path().stem
            )

            return Document(
                id=source.path().stem,
                title=title,
                source=str(
                    source.path(),
                ),
                language="unknown",
                pages=pages,
                metadata=metadata,
            )

        finally:

            self.backend.close()