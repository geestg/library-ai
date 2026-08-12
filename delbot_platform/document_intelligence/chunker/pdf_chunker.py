from __future__ import annotations

from ..models.paragraph import Paragraph
from ..models.parsed_document import ParsedDocument
from ..models.semantic_chunk import SemanticChunk
from ..models.semantic_chunk_collection import SemanticChunkCollection
from .document_chunker import DocumentChunker


class PDFChunker(DocumentChunker):

    def chunk(
        self,
        document: ParsedDocument,
    ) -> SemanticChunkCollection:

        chunks = []

        for page in document.pages:
            for block in page.blocks:

                text = " ".join(
                    span.text
                    for line in block.lines
                    for span in line.spans
                    if span.text.strip()
                ).strip()

                if not text:
                    continue

                paragraph = Paragraph(
                    text=text,
                    page_number=page.page_number,
                    heading=None,
                )

                chunks.append(
                    SemanticChunk(
                        text=text,
                        page_start=page.page_number,
                        page_end=page.page_number,
                        paragraphs=[paragraph],
                        heading=None,
                        metadata={},
                    )
                )

        return SemanticChunkCollection(
            chunks=chunks,
        )
