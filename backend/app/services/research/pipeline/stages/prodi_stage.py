from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.prodi_engine import (
    run_prodi_pipeline,
)


class ProdiStage(BaseStage):

    # =====================================
    # STAGE METADATA
    # =====================================

    name = "prodi"

    priority = 50

    requires = [

        "competency",

        "domain",

    ]

    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        context,
    ):

        run_prodi_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Prodi completed",

        )
