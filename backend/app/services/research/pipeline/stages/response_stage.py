from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.response_engine import (
    build_research_response,
)


class ResponseStage(
    BaseStage
):

    name = "response"

    def execute(
        self,
        context,
    ):

        if context.response is not None:

            return StageResult(

                success=True,

                message="Existing response preserved",

                metadata={

                    "response_source":
                        "specialized",

                },

            )

        if context.llm_stream is not None:

            return StageResult(

                success=True,

                message="Response deferred to stream consumer",

                metadata={

                    "response_source":
                        "stream",

                },

            )

        context.response = (
            build_research_response(
                context
            )
        )

        return StageResult(

            success=True,

            message="Response built",

            metadata={

                "response_source":
                    "research",

            },

        )