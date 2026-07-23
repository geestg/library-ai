from __future__ import annotations

from pathlib import Path

from delbot_platform.document_intelligence.backend.pdf.pymupdf_backend import (
    PyMuPDFBackend,
)
from delbot_platform.document_intelligence.loader.document_loader import (
    DocumentLoader,
)
from delbot_platform.document_intelligence.loader.loaded_document import (
    LoadedDocument,
)


class PDFLoader(DocumentLoader):

    def load(
        self,
        source: Path,
    ) -> LoadedDocument:

        backend = PyMuPDFBackend()

        document = backend.open(
            source,
        )

        return LoadedDocument(
            source_path=source,
            backend_document=document,
        )
