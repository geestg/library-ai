from __future__ import annotations

from delbot_platform.documents.classification.heading import (
    HeadingClassifier,
)

from delbot_platform.documents.extraction.service import (
    DocumentExtractionService,
)

from delbot_platform.documents.models.block import (
    Block,
)

from delbot_platform.documents.structure.section.builder import (
    SectionBuilder,
)

from delbot_platform.documents.structure.section.section import (
    DocumentSection,
)


class DocumentPreprocessingPipeline:
    """
    Complete preprocessing pipeline.

    PDF
      │
      ▼
    Extraction
      │
      ▼
    Heading Classification
      │
      ▼
    Section Builder
    """

    def __init__(
        self,
    ) -> None:

        self.extractor = DocumentExtractionService()

        self.heading = HeadingClassifier()

        self.sections = SectionBuilder()

    def process(
        self,
        *,
        document_id: str,
        source: str,
        pdf_path: str,
    ) -> list[DocumentSection]:

        blocks = self.extractor.extract(
            pdf_path,
        )

        classified: list[Block] = []

        for block in blocks:

            block.type = self.heading.classify(
                block,
            )

            classified.append(
                block,
            )

        return self.sections.build(

            document_id=document_id,

            source=source,

            blocks=classified,

        )