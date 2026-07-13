import json

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)


def build_context(
    query: str = "analisis artificial intelligence",
    active_document_ids=None,
):

    return ResearchContext(

        query=query,

        session_id="test-session",

        top_k=5,

        mode="analysis",

        active_document_ids=(
            active_document_ids or []
        ),

    )


def parse_ndjson(
    content: str,
):

    return [

        json.loads(line)

        for line in content.splitlines()

        if line.strip()

    ]


class SuccessfulStage(
    BaseStage
):

    name = "successful"

    def execute(
        self,
        context,
    ):

        context.analysis = (
            "Pipeline completed"
        )

        return StageResult(

            success=True,

            message="Successful stage completed",

        )


class FailingStage(
    BaseStage
):

    name = "failing"

    def execute(
        self,
        context,
    ):

        raise ValueError(
            "Synthetic pipeline failure"
        )