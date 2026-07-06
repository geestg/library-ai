from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.literature_engine import (
    run_literature_review_pipeline,
)


class LiteratureStage(
    BaseStage
):

    name = "literature"

    def execute(
        self,
        context,
    ):

        result = run_literature_review_pipeline(
            context
        )

        if result is None:

            return StageResult(

                success=True,

                message="Literature review skipped",

            )

        context.response = result

        return StageResult(

            success=True,

            message="Literature review generated",

            stop_pipeline=True,

        )