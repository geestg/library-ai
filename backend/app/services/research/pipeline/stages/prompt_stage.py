from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.prompt_engine import (
    run_prompt_pipeline,
)


class PromptStage(
    BaseStage
):

    name = "prompt"

    def execute(
        self,
        context,
    ):

        run_prompt_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Prompt generated",

            metadata={

                "prompt_length":

                len(
                    context.prompt
                )

            }

        )

