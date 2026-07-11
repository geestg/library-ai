from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.evidence_engine import (
    run_evidence_pipeline,
)


class EvidenceStage(BaseStage):

    # =====================================
    # STAGE METADATA
    # =====================================

    name = "evidence"

    priority = 30

    requires = [

        "search",

        "domain",

    ]

    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        context,
    ):

        run_evidence_pipeline(
            context
        )

        return StageResult(

            success=True,

            message="Evidence completed",

        )
