from __future__ import annotations

from ...documents.models.document import Document

from delbot_platform.ai.embedding.embedding_builder import (
    EmbeddingBuilder,
)

from ..chunker import PDFChunker
from ..indexer import PDFIndexer
from ..loader import PDFLoader
from ..metadata import PDFMetadata
from ..parser import PDFParser

from .document_pipeline import DocumentPipeline
from .pipeline_result import PipelineResult


class PDFPipeline(DocumentPipeline):

    def process(
        self,
        document: Document,
    ) -> PipelineResult:

        loaded = PDFLoader().load(document)
        parsed = PDFParser().parse(loaded)

        chunked = PDFChunker().chunk(parsed)
        metadata = PDFMetadata().extract(chunked)
        indexed = PDFIndexer().index(metadata)

        requests = EmbeddingBuilder().build(indexed)

        indexed.metadata["embedding_requests"] = requests

        return PipelineResult(
            source_document=document,
            indexed_document=indexed,
            success=True,
        )
