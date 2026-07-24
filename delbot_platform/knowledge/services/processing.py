from __future__ import annotations

from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
)

from delbot_platform.knowledge.pipeline import (
    KnowledgePipeline,
)

from delbot_platform.knowledge.pipeline.models import (
    KnowledgeArtifact,
)

from delbot_platform.knowledge.pipeline import (
    KnowledgePipelineResult,
)


class KnowledgeService:

    def __init__(
        self,
    ) -> None:

        self.pipeline = (
            KnowledgePipeline()
        )

    def process(
        self,
        artifact: DocumentIndexArtifact,
    ) -> tuple[
        KnowledgeArtifact,
        KnowledgePipelineResult,
    ]:

        return self.pipeline.process_with_summary(
            artifact,
        )
