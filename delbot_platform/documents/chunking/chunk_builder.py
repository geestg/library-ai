from __future__ import annotations

from uuid import uuid4

from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)

from delbot_platform.documents.chunking.policy.policy import (
    ChunkPolicy,
)

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)

from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)


class ChunkBuilder:
    """
    Build semantic chunks from document sections.

    Each chunk keeps document identity,
    page information and section hierarchy.
    """

    def __init__(
        self,
        policy: ChunkPolicy | None = None,
    ) -> None:

        self.policy = policy or ChunkPolicy()

    def build(
        self,
        sections: list[DocumentSection],
    ) -> list[DocumentChunk]:

        chunks: list[DocumentChunk] = []

        for section in sections:

            text = section.text.strip()

            if not text:

                continue

            start = 0

            length = len(text)

            while start < length:

                end = min(

                    start
                    + self.policy.max_characters,

                    length,

                )

                chunk_text = text[start:end]

                metadata = ChunkMetadata(

                    document_id=section.document_id,

                    source=section.source,

                    section=section.title,

                    level=section.level,

                    page_start=section.page_start,

                    page_end=section.page_end,

                    chapter=section.chapter,

                )

                chunk = DocumentChunk(

                    id=str(
                        uuid4(),
                    ),

                    document_id=section.document_id,

                    text=chunk_text,

                    page_start=section.page_start,

                    page_end=section.page_end,

                    metadata=metadata,

                )

                chunks.append(
                    chunk,
                )

                if end >= length:

                    break

                start = max(

                    0,

                    end
                    - self.policy.overlap_characters,

                )

        total = len(chunks)

        for index, chunk in enumerate(chunks):

            chunk.metadata.chunk_index = index

            chunk.metadata.total_chunks = total

        return chunks