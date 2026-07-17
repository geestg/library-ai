from __future__ import annotations

import time

from delbot_platform.documents.chunking import (
    ChunkBuilder,
)

from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)

from delbot_platform.documents.pipeline.models.index_result import (
    DocumentIndexResult,
)

from delbot_platform.documents.pipeline.preprocessing import (
    DocumentPreprocessingPipeline,
)

from delbot_platform.documents.registry.manager import (
    DocumentRegistryManager,
)


class DocumentIndexingPipeline:
    """
    Canonical Document Indexing Pipeline.

    Flow

        Registry
            │
            ▼
        Preprocessing
            │
            ▼
        DocumentSection[]
            │
            ▼
        ChunkBuilder
            │
            ▼
        EmbeddingPipeline
            │
            ▼
        DocumentIndexResult
    """

    def __init__(
        self,
    ) -> None:

        self.registry = (
            DocumentRegistryManager()
        )

        self.preprocessing = (
            DocumentPreprocessingPipeline()
        )

        self.chunk_builder = (
            ChunkBuilder()
        )

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

        sections = self.preprocessing.process(

            document_id=document.id,

            source=document.source,

            pdf_path=pdf_path,

        )

        chunks = self.chunk_builder.build(
            sections,
        )

        vectors = await self.embedding.run(
            chunks,
        )

        elapsed = (
            time.perf_counter()
            - started
        )

        block_count = sum(

            section.block_count

            for section in sections

        )

        page_count = max(

            (

                section.page_end

                for section in sections

            ),

            default=0,

        )

        return DocumentIndexResult(

            document_id=document.id,

            source=document.source,

            pages=page_count,

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