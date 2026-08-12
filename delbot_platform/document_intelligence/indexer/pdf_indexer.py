from __future__ import annotations

from ..metadata.metadata_result import MetadataResult
from .document_indexer import DocumentIndexer
from .indexed_document import IndexedDocument


class PDFIndexer(DocumentIndexer):

    def index(
        self,
        document: MetadataResult,
    ) -> IndexedDocument:

        return IndexedDocument(
            source_document=document.source_document,
            index=document.sections,
            metadata=document.metadata,
        )
