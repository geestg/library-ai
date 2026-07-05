from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.thesis_idea_engine import (
    run_thesis_idea_pipeline,
)


class ThesisIdeaStage(
    BaseStage
):

    name = "thesis_idea"

    def execute(
        self,
        context,
    ):

        result = run_thesis_idea_pipeline(
            context
        )

        if result is None:

            return StageResult(

                success=True,

                message="Thesis idea skipped",

            )

        context.response = result

        return StageResult(

            success=True,

            message="Thesis ideas generated",

            stop_pipeline=True,

        )