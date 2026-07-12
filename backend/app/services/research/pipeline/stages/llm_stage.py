from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.llm_engine import (
    run_llm_pipeline,
)


class LLMStage(
    BaseStage
):

    name = "llm"

    def __init__(
        self,
        stream: bool = False,
    ):

        self.stream = stream

    def execute(
        self,
        context,
    ):

        if self.stream:

            context.llm_stream = (
                run_llm_pipeline(

                    context,

                    stream=True,

                )
            )

        else:

            run_llm_pipeline(

                context,

                stream=False,

            )

        return StageResult(

            success=True,

            message="LLM completed",

        )

