from __future__ import annotations

from delbot_platform.document_intelligence.loader.loaded_document import (
    LoadedDocument,
)
from delbot_platform.document_intelligence.parser.document_parser import (
    DocumentParser,
)
from delbot_platform.document_intelligence.pipeline.pipeline_stage import (
    PipelineStage,
)


class ParserStage(PipelineStage):

    def __init__(
        self,
        parser: DocumentParser,
    ) -> None:
        self._parser = parser

    def process(
        self,
        data: LoadedDocument,
    ):
        return self._parser.parse(
            data,
        )
