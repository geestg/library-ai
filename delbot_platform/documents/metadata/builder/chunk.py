from __future__ import annotations

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)


class ChunkMetadataBuilder:
    """
    Canonical builder for ChunkMetadata.

    Responsibilities
    ----------------
    - Build canonical ChunkMetadata.
    - Normalize metadata for vector storage.
    - Keep embedding pipeline independent from chunk models.

    This builder is the single public entrypoint for creating
    metadata attached to semantic chunks.
    """

    def build(
        self,
        chunk,
    ) -> ChunkMetadata:

        page_start = getattr(chunk, "page_start", 0)
        page_end = getattr(chunk, "page_end", page_start)

        section_title = getattr(chunk, "section_title", None)

        chapter = getattr(chunk, "chapter", None)

        level = getattr(chunk, "level", None)

        

        token_count = getattr(
            chunk,
            "token_count",
            len(getattr(chunk, "text", "").split()),
        )

        character_count = len(
            getattr(chunk, "text", "")
        )

        return ChunkMetadata(
            document_id=getattr(chunk, "document_id"),
            chunk_id=getattr(chunk, "chunk_id"),
            source=getattr(chunk, "source", "repository"),
            page_start=page_start,
            page_end=page_end,
            section_title=section_title,
            chapter=chapter,
            level=level,
            
            token_count=token_count,
            character_count=character_count,
        )
