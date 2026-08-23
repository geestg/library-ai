from __future__ import annotations

from delbot_platform.document_intelligence.builder.document_builder import (
    DocumentBuilder,
)
from delbot_platform.document_intelligence.models.parsed_document import (
    ParsedDocument,
)
from delbot_platform.document_intelligence.pipeline.pipeline_stage import (
    PipelineStage,
)


class BuilderStage(PipelineStage):

    def __init__(
        self,
        builder: DocumentBuilder,
    ) -> None:
        self._builder = builder

    def process(
        self,
        data: ParsedDocument,
    ):
        return self._builder.build(
            data,
        )
