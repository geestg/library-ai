from __future__ import annotations

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)

from delbot_platform.documents.models.block import (
    Block,
)

from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)


class SectionBuilder:
    """
    Build logical document sections from classified blocks.

    Input:
        Block sequence

    Output:
        DocumentSection sequence

    Every produced section already contains all metadata
    required by downstream chunking and indexing.
    """

    def build(
        self,
        *,
        document_id: str,
        source: str,
        blocks: list[Block],
    ) -> list[DocumentSection]:

        sections: list[DocumentSection] = []

        current: DocumentSection | None = None

        for block in blocks:

            #
            # New heading starts a new section
            #

            if (
                block.type
                == DocumentBlockType.HEADING
            ):

                if current and current:

                    sections.append(
                        current,
                    )

                current = DocumentSection(

                    document_id=document_id,

                    source=source,

                    title=block.text.strip(),

                    chapter=block.text.strip(),

                    level=1,

                    page_start=block.page,

                    page_end=block.page,

                )

                continue

            #
            # First paragraph before heading
            #

            if current is None:

                current = DocumentSection(

                    document_id=document_id,

                    source=source,

                    title="Introduction",

                    chapter=None,

                    level=0,

                    page_start=block.page,

                    page_end=block.page,

                )

            current.add_block(
                block,
            )

        if current and current:

            sections.append(
                current,
            )

        return sections