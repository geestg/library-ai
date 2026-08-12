from __future__ import annotations

from ..models.semantic_chunk_collection import (
    SemanticChunkCollection,
)
from .document_metadata import DocumentMetadata
from .metadata_result import MetadataResult


class PDFMetadata(DocumentMetadata):

    def extract(
        self,
        document: SemanticChunkCollection,
    ) -> MetadataResult:

        chunks = document.chunks

        page_start = None
        page_end = None

        if chunks:
            page_start = min(
                chunk.page_start
                for chunk in chunks
            )

            page_end = max(
                chunk.page_end
                for chunk in chunks
            )

        metadata = {
            "chunk_count": len(chunks),
            "page_start": page_start,
            "page_end": page_end,
        }

        return MetadataResult(
            source_document=document,
            metadata=metadata,
            sections=chunks,
        )
