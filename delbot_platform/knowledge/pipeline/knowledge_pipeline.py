from __future__ import annotations

from delbot_platform.documents.pipeline.models import (
    DocumentIndexArtifact,
)

from delbot_platform.knowledge.pipeline.models import (
    KnowledgeArtifact,
)

from delbot_platform.knowledge.pipeline.pipeline_context import (
    KnowledgePipelineContext,
)

from delbot_platform.knowledge.pipeline.pipeline_result import (
    KnowledgePipelineResult,
)


class KnowledgePipeline:

    def process(
        self,
        artifact: DocumentIndexArtifact,
    ) -> KnowledgeArtifact:

        _ = KnowledgePipelineContext(
            document_id=artifact.document_id,
            source=artifact.source,
            chunk_count=artifact.chunk_count,
            vector_count=artifact.vector_count,
        )

        return KnowledgeArtifact(
            document_index=artifact,
        )

    def summarize(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgePipelineResult:

        return KnowledgePipelineResult(
            document_id=artifact.document_id,
            extracted_entities=len(
                artifact.entities,
            ),
            extracted_relations=len(
                artifact.relations,
            ),
            success=True,
        )

    def process_with_summary(
        self,
        artifact: DocumentIndexArtifact,
    ) -> tuple[
        KnowledgeArtifact,
        KnowledgePipelineResult,
    ]:

        knowledge = self.process(
            artifact,
        )

        summary = self.summarize(
            knowledge,
        )

        return (
            knowledge,
            summary,
        )
