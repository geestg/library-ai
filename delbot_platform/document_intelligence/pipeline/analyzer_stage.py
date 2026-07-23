from __future__ import annotations

from delbot_platform.document_intelligence.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.document_intelligence.pipeline.pipeline_stage import (
    PipelineStage,
)


class AnalyzerStage(PipelineStage):

    def __init__(
        self,
        *analyzers: DocumentAnalyzer,
    ) -> None:

        self._analyzers = list(
            analyzers,
        )

    def process(
        self,
        data: ParsedDocument,
    ) -> ParsedDocument:

        document = data

        for analyzer in self._analyzers:
            document = analyzer.analyze(
                document,
            )

        return document
