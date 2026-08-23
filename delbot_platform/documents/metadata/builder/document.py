from __future__ import annotations

from delbot_platform.documents.metadata.document_metadata import (
    DocumentMetadata,
)

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)


class DocumentMetadataBuilder:
    """
    Build canonical metadata for a document.

    This metadata accompanies every indexed document and
    becomes the source for retrieval and citation.
    """

    def build(
        self,
        record: DocumentRecord,
        *,
        pages: int,
        blocks: int,
        sections: int,
        chunks: int,
    ) -> DocumentMetadata:

        return DocumentMetadata(

            document_id=record.id,

            source=record.source,

            pages=pages,

            blocks=blocks,

            sections=sections,

            chunks=chunks,

        )