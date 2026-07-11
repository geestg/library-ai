from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.domain_engine import (
    run_domain_pipeline,
)


class DomainStage(BaseStage):

    # =====================================
    # STAGE METADATA
    # =====================================

    name = "domain"

    priority = 20

    requires = [
        "search",
    ]

    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        context,
    ):

        run_domain_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Domain completed",

        )
