from __future__ import annotations

from delbot_platform.documents.metadata.document_metadata import (
    DocumentMetadata,
)
from delbot_platform.documents.metadata.metadata_extractor import (
    MetadataExtractor,
)
from delbot_platform.documents.registry.document import (
    DocumentRecord,
)


class DocumentMetadataBuilder:
    """
    Canonical metadata builder.

    Responsibilities
    ----------------
    - Build final DocumentMetadata.
    - Use MetadataExtractor for content-derived metadata.
    - Merge repository metadata.
    - Compute indexing statistics.

    This class is the only public metadata builder used by the
    indexing pipeline.
    """

    def __init__(
        self,
        extractor: MetadataExtractor | None = None,
    ) -> None:

        self._extractor = (
            extractor
            if extractor is not None
            else MetadataExtractor()
        )

    def build(
        self,
        record: DocumentRecord,
        *,
        sections: list,
        chunks: list,
    ) -> DocumentMetadata:

        pages = self._collect_pages(sections)

        metadata = self._extractor.extract(
            document_id=record.id,
            pages=pages,
        )

        metadata.source = record.source

        metadata.pages = max(
            metadata.pages,
            self._page_count(sections),
        )

        metadata.blocks = self._block_count(
            sections,
        )

        metadata.sections = len(
            sections,
        )

        metadata.chunks = len(
            chunks,
        )

        if record.title:
            metadata.title = record.title

        if record.author:
            metadata.authors = [
                record.author,
            ]

        if record.year:
            metadata.year = record.year

        return metadata

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _collect_pages(
        self,
        sections: list,
    ) -> list[str]:

        pages: list[str] = []

        for section in sections:

            text = getattr(
                section,
                "text",
                "",
            )

            pages.append(text)

        return pages

    def _page_count(
        self,
        sections: list,
    ) -> int:

        page_count = 0

        for section in sections:

            page_count = max(
                page_count,
                getattr(
                    section,
                    "page_end",
                    0,
                ),
            )

        return page_count

    def _block_count(
        self,
        sections: list,
    ) -> int:

        count = 0

        for section in sections:

            count += len(
                getattr(
                    section,
                    "blocks",
                    [],
                ),
            )

        return count
