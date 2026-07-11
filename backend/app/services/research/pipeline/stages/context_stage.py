from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.context_engine import (
    run_context_pipeline,
)


class ContextStage(
    BaseStage
):

    name = "context"

    def execute(
        self,
        context,
    ):

        run_context_pipeline(
            context
        )

        return StageResult(
            success=True,
            message="Context built",
            metadata={

                "citations":

                len(
                    context.citations
                ),

                "sources":

                len(
                    context.theses
                )

            }

        )
