from __future__ import annotations

from delbot_platform.documents.models.document_chunk import (
    DocumentChunk,
)


class ContextBuilder:
    """
    Canonical Context Builder.

    Input
        list[DocumentChunk]

    Output
        str
    """

    def build(
        self,
        chunks: list[DocumentChunk],
    ) -> str:

        if not chunks:
            return ""

        contexts: list[str] = []

        for chunk in chunks:

            metadata = chunk.metadata

            source = chunk.document_id

            if metadata is not None and metadata.source:
                source = metadata.source

            section = ""

            if chunk.section_title:
                section = chunk.section_title

            header = (
                f"[Document: {source}] "
                f"[Pages: {chunk.page_start}-{chunk.page_end}]"
            )

            if section:
                header += f" [Section: {section}]"

            contexts.append(
                "\n".join(
                    [
                        header,
                        chunk.text.strip(),
                    ]
                )
            )

        return "\n\n============================================================\n\n".join(
            contexts
        )
