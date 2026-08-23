from __future__ import annotations

from delbot_platform.document_intelligence.analyzer.heading_detector import (
    HeadingDetector,
)
from delbot_platform.document_intelligence.analyzer.page_text_analyzer import (
    PageTextAnalyzer,
)
from delbot_platform.document_intelligence.builder.default_document_builder import (
    DefaultDocumentBuilder,
)
from delbot_platform.document_intelligence.loader.pdf_loader import (
    PDFLoader,
)
from delbot_platform.document_intelligence.parser.pdf_document_parser import (
    PDFDocumentParser,
)
from delbot_platform.document_intelligence.pipeline.analyzer_stage import (
    AnalyzerStage,
)
from delbot_platform.document_intelligence.pipeline.builder_stage import (
    BuilderStage,
)
from delbot_platform.document_intelligence.pipeline.document_pipeline import (
    DocumentPipeline,
)
from delbot_platform.document_intelligence.pipeline.parser_stage import (
    ParserStage,
)
from delbot_platform.document_intelligence.processor.document_processor import (
    DocumentProcessor,
)


class DocumentProcessorFactory:

    @staticmethod
    def create() -> DocumentProcessor:

        pipeline = DocumentPipeline(
            ParserStage(
                PDFDocumentParser(),
            ),
            AnalyzerStage(
                PageTextAnalyzer(),
                HeadingDetector(),
            ),
            BuilderStage(
                DefaultDocumentBuilder(),
            ),
        )

        return DocumentProcessor(
            loader=PDFLoader(),
            pipeline=pipeline,
        )
