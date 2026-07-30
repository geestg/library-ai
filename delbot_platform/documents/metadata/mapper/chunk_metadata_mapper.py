from __future__ import annotations

from dataclasses import asdict
from typing import Any

from delbot_platform.documents.metadata.chunk_metadata import (
    ChunkMetadata,
)


class ChunkMetadataMapper:
    """
    Canonical mapper between storage payloads and ChunkMetadata.

    Storage repositories must exchange dictionaries.
    Documents domain uses ChunkMetadata exclusively.
    """

    @staticmethod
    def from_payload(
        payload: dict[str, Any] | None,
    ) -> ChunkMetadata:

        payload = payload or {}

        return ChunkMetadata(
            document_id=payload.get(
                "document_id",
                "",
            ),
            chunk_id=payload.get(
                "chunk_id",
                "",
            ),
            source=payload.get(
                "source",
                "",
            ),
            section_title=payload.get(
                "section_title",
                "",
            ),
            chapter=payload.get(
                "chapter",
            ),
            level=payload.get(
                "level",
                0,
            ),
            page_start=payload.get(
                "page_start",
                0,
            ),
            page_end=payload.get(
                "page_end",
                0,
            ),
            token_count=payload.get(
                "token_count",
                0,
            ),
            character_count=payload.get(
                "character_count",
                0,
            ),
            language=payload.get(
                "language",
                "id",
            ),
            tags=payload.get(
                "tags",
                [],
            ),
            keywords=payload.get(
                "keywords",
                [],
            ),
            embedding_model=payload.get(
                "embedding_model",
            ),
            embedding_version=payload.get(
                "embedding_version",
            ),
            checksum=payload.get(
                "checksum",
            ),
        )

    @staticmethod
    def to_payload(
        metadata: ChunkMetadata,
        **extra: Any,
    ) -> dict[str, Any]:

        payload = asdict(
            metadata,
        )

        payload.update(extra)

        return payload
