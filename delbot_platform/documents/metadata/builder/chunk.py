from __future__ import annotations

from delbot_platform.documents.chunking.chunk import (
    DocumentChunk,
)

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)

from delbot_platform.documents.registry.document import (
    DocumentRecord,
)

from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)


class ChunkMetadataBuilder:
    """
    Build metadata attached to every semantic chunk.
    """

    def build(
        self,
        *,
        record: DocumentRecord,
        section: DocumentSection,
        chunk: DocumentChunk,
        chunk_index: int,
        total_chunks: int,
    ) -> ChunkMetadata:

        return ChunkMetadata(

            document_id=record.id,

            source=record.source,

            section=section.title,

            level=section.level,

            chapter=section.chapter,

            page_start=chunk.page_start,

            page_end=chunk.page_end,

            chunk_index=chunk_index,

            total_chunks=total_chunks,

        )