from __future__ import annotations

import time

import fitz

from delbot_platform.documents.loader.pdf import (
    PDFLoader,
)
from delbot_platform.documents.extraction.block import (
    BlockExtractor,
)
from delbot_platform.documents.classification.heading import (
    HeadingClassifier,
)
from delbot_platform.documents.classification.page_classifier import (
    PageClassifier,
)
from delbot_platform.documents.structure.builder import (
    SectionBuilder,
)
from delbot_platform.documents.structure.hierarchy import (
    SectionHierarchyBuilder,
)
from delbot_platform.documents.chunking.builder import (
    ChunkBuilder,
)
from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)
from delbot_platform.documents.pipeline.models.index_result import (
    DocumentIndexResult,
)
from delbot_platform.documents.registry.manager import (
    DocumentRegistryManager,
)


class DocumentIndexingPipeline:

    def __init__(
        self,
    ) -> None:

        self.registry = DocumentRegistryManager()

        self.loader = PDFLoader()

        self.extractor = BlockExtractor()

        self.heading = HeadingClassifier()

        self.page_classifier = PageClassifier()

        self.section_builder = SectionBuilder()

        self.hierarchy_builder = (
            SectionHierarchyBuilder()
        )

        self.chunk_builder = ChunkBuilder()

        self.embedding = (
            EmbeddingPipeline()
        )

    async def index(
        self,
        pdf_path: str,
    ) -> DocumentIndexResult:

        started = time.perf_counter()

        document = self.registry.resolve(
            pdf_path,
        )

        pdf = self.loader.load(
            pdf_path,
        )

        items = []

        block_count = 0

        for page in pdf:

            blocks = self.extractor.extract(
                page,
            )

            block_count += len(
                blocks,
            )

            page_type = (
                self.page_classifier.classify(
                    page,
                )
            )

            for block in blocks:

                items.append(

                    self.heading.classify(

                        block,

                        page_type,
                    )

                )

        sections = (
            self.section_builder.build(
                items,
            )
        )

        hierarchy = (
            self.hierarchy_builder.build(
                sections,
            )
        )

        chunks = (
            self.chunk_builder.build(
                hierarchy,
            )
        )

        vectors = await self.embedding.embed(
            chunks,
        )

        elapsed = (
            time.perf_counter()
            - started
        )

        return DocumentIndexResult(

            document_id=document.id,

            source=document.source,

            pages=len(pdf),

            blocks=block_count,

            sections=len(
                sections,
            ),

            chunks=len(
                chunks,
            ),

            vectors=len(
                vectors,
            ),

            elapsed=elapsed,

            success=True,
        )