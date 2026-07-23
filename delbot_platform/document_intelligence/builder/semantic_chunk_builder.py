from __future__ import annotations

from delbot_platform.document_intelligence.models.paragraph import (
    Paragraph,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.document_intelligence.models.semantic_chunk import (
    SemanticChunk,
)
from delbot_platform.document_intelligence.models.semantic_chunk_collection import (
    SemanticChunkCollection,
)


class SemanticChunkBuilder:
    """
    Build semantic chunks from paragraphs.

    MVP Strategy
    ------------

    ParagraphCollection
            ↓
    Merge paragraphs
            ↓
    ~900 characters
            ↓
    SemanticChunkCollection
    """

    _MAX_CHARACTERS = 900

    def build(
        self,
        document: ParsedDocument,
    ) -> ParsedDocument:

        paragraphs = document.metadata[
            "paragraph_collection"
        ]

        collection = SemanticChunkCollection()

        buffer: list[Paragraph] = []
        current_size = 0

        for paragraph in paragraphs:

            if (
                buffer
                and paragraph.page_number
                != buffer[-1].page_number
            ):

                self._flush(
                    buffer,
                    collection,
                )

                buffer = []
                current_size = 0

            paragraph_size = len(
                paragraph.text,
            )

            if (
                buffer
                and current_size + paragraph_size
                > self._MAX_CHARACTERS
            ):

                self._flush(
                    buffer,
                    collection,
                )

                buffer = []
                current_size = 0

            buffer.append(
                paragraph,
            )

            current_size += (
                paragraph_size + 1
            )

        if buffer:

            self._flush(
                buffer,
                collection,
            )

        document.metadata[
            "semantic_chunk_collection"
        ] = collection

        return document

    def _flush(
        self,
        paragraphs: list[Paragraph],
        collection: SemanticChunkCollection,
    ) -> None:

        if not paragraphs:
            return

        text = "\n\n".join(
            paragraph.text
            for paragraph in paragraphs
        )

        chunk = SemanticChunk(
            text=text,
            page_start=paragraphs[0].page_number,
            page_end=paragraphs[-1].page_number,
            paragraphs=list(
                paragraphs,
            ),
            heading=None,
        )

        collection.add(
            chunk,
        )
