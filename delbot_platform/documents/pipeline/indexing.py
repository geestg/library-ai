from __future__ import annotations

import time

from delbot_platform.documents.chunking import (
    ChunkBuilder,
)
from delbot_platform.documents.embedding.pipeline.pipeline import (
    EmbeddingPipeline,
)
from delbot_platform.documents.embedding.mapper import (
    EmbeddingVectorMapper,
)
from delbot_platform.documents.metadata.builder.document import (
    DocumentMetadataBuilder,
)
from delbot_platform.documents.metadata.repository import (
    DocumentMetadataRepository,
)
from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
    DocumentIndexResult,
)
from delbot_platform.documents.pipeline.preprocessing import (
    DocumentPreprocessingPipeline,
)
from delbot_platform.documents.registry.manager import (
    DocumentRegistryManager,
)
from delbot_platform.vectorstore import (
    QdrantRepository,
)


class DocumentIndexingPipeline:

    def __init__(
        self,
    ) -> None:

        self.registry = DocumentRegistryManager()

        self.preprocessing = (
            DocumentPreprocessingPipeline()
        )

        self.chunk_builder = ChunkBuilder()

        self.metadata_builder = (
            DocumentMetadataBuilder()
        )

        self.metadata_repository = (
            DocumentMetadataRepository()
        )

        self.embedding = EmbeddingPipeline()

        self.vectorstore = (
            QdrantRepository()
        )

    async def index(
        self,
        pdf_path: str,
    ) -> DocumentIndexArtifact:

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

        metadata = self.metadata_builder.build(
            record=document,
            sections=sections,
            chunks=chunks,
        )

        self.metadata_repository.save(
            metadata,
        )

        vectors = await self.embedding.run(
            chunks,
        )

        vector_records = (
            EmbeddingVectorMapper.to_vector_records(
                vectors,
            )
        )

        self.vectorstore.save(
            vector_records,
        )

        return DocumentIndexArtifact(
            document=document,
            metadata=metadata,
            sections=sections,
            chunks=chunks,
            vectors=vectors,
        )

    def summarize(
        self,
        artifact: DocumentIndexArtifact,
        elapsed: float,
    ) -> DocumentIndexResult:

        return DocumentIndexResult(
            document_id=artifact.document_id,
            source=artifact.source,
            pages=artifact.page_count,
            blocks=artifact.block_count,
            sections=artifact.section_count,
            chunks=artifact.chunk_count,
            vectors=artifact.vector_count,
            elapsed=elapsed,
            success=True,
        )

    async def index_with_summary(
        self,
        pdf_path: str,
    ) -> tuple[
        DocumentIndexArtifact,
        DocumentIndexResult,
    ]:

        started = time.perf_counter()

        artifact = await self.index(
            pdf_path,
        )

        elapsed = (
            time.perf_counter()
            - started
        )

        summary = self.summarize(
            artifact,
            elapsed,
        )

        return (
            artifact,
            summary,
        )
