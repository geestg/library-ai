from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.competency_engine import (
    run_competency_pipeline,
)


class CompetencyStage(BaseStage):

    # =====================================
    # STAGE METADATA
    # =====================================

    name = "competency"

    priority = 40

    requires = [

        "evidence",

    ]

    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        context,
    ):

        run_competency_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Competency completed",

        )