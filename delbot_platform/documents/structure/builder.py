from __future__ import annotations

from delbot_platform.documents.classification.document_type import (
    DocumentBlockType,
)

from delbot_platform.documents.classification.page_region import (
    PageRegion,
)

from delbot_platform.documents.classification.heading_score import (
    HeadingScorer,
)

from delbot_platform.documents.structure.section import (
    Section,
)

from delbot_platform.documents.structure.document_structure import (
    DocumentStructure,
)


class SectionBuilder:


    def __init__(
        self,
        heading_threshold: float = 0.75,
    ) -> None:

        self.heading_threshold = heading_threshold

        self.heading_scorer = HeadingScorer()



    def build(
        self,
        classified_blocks,
    ) -> DocumentStructure:


        structure = DocumentStructure()

        current = None


        for block, block_type, region in classified_blocks:


            if region == PageRegion.COVER:

                section = Section(
                    title=block.text,
                    level=0,
                )

                section.blocks.append(
                    block,
                )

                structure.cover.append(
                    section,
                )

                continue



            if region == PageRegion.FRONT_MATTER:

                section = Section(
                    title=block.text,
                    level=0,
                )

                section.blocks.append(
                    block,
                )

                structure.front_matter.append(
                    section,
                )

                continue



            heading_score = self.heading_scorer.score(
                text=block.text,
                font_size=block.font_size,
                bold=block.bold,
            )


            is_heading = (
                heading_score
                >= self.heading_threshold
            )


            if is_heading:


                current = Section(
                    title=block.text,
                    level=1,
                )


                structure.sections.append(
                    current,
                )

                continue



            if current is None:


                current = Section(
                    title="Document",
                    level=0,
                )


                structure.sections.append(
                    current,
                )


            current.blocks.append(
                block,
            )


        return structure