from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.comparison_engine import (
    run_comparison_pipeline,
)


class ComparisonStage(
    BaseStage
):

    name = "comparison"

    def execute(
        self,
        context,
    ):

        result = run_comparison_pipeline(
            context
        )

        if result is None:

            return StageResult(
                success=True,
                message="Comparison skipped",
            )

        context.response = result

        return StageResult(

            success=True,

            message="Comparison completed",

            stop_pipeline=True,

        )
