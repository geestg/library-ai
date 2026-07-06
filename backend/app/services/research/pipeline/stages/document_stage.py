from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.document_engine import (
    run_document_analysis,
)


class DocumentStage(
    BaseStage
):

    name = "document"

    def execute(
        self,
        context,
    ):

        if not context.active_document_ids:

            return StageResult(

                success=True,

                message="Document stage skipped",

            )

        result = run_document_analysis(

            query=context.query,

            session_id=context.session_id,

            active_document_ids=(
                context.active_document_ids
            ),

        )

        if result is None:

            return StageResult(

                success=True,

                message="No active document",

            )

        context.response = result

        return StageResult(

            success=True,

            message="Document analysis completed",

            metadata={

                "documents":
                    len(
                        result.get(
                            "documents",
                            [],
                        )
                    ),

            },

            stop_pipeline=True,

        )