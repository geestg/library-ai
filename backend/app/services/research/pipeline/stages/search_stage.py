from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.search_engine import (
    run_search_pipeline,
)


class SearchStage(BaseStage):

    name = "search"

    priority = 10

    requires = []

    def execute(
        self,
        context,
    ):

        run_search_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Search completed",

            metadata={

                "retrieved":

                len(context.theses)

            }

        )