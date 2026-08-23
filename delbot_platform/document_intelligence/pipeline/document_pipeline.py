from __future__ import annotations

from delbot_platform.document_intelligence.pipeline.pipeline_stage import (
    PipelineStage,
)


class DocumentPipeline:

    def __init__(
        self,
        *stages: PipelineStage,
    ) -> None:

        self._stages = list(
            stages,
        )

    def process(
        self,
        data,
    ):

        result = data

        for stage in self._stages:

            result = stage.process(
                result,
            )

        return result
