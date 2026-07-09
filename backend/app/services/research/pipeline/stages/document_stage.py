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

        # =====================================
        # SKIP WITHOUT ACTIVE DOCUMENTS
        # =====================================

        if not context.active_document_ids:

            return StageResult(

                success=True,

                message=(
                    "Document stage skipped"
                ),

            )

        # =====================================
        # RESOLVE PROGRESS CALLBACK
        # =====================================

        progress_callback = getattr(

            context,

            "progress_callback",

            None,

        )

        # =====================================
        # DOCUMENT ANALYSIS
        # =====================================

        result = run_document_analysis(

            query=context.query,

            session_id=context.session_id,

            active_document_ids=(
                context.active_document_ids
            ),

            progress_callback=(
                progress_callback
            ),

        )

        # =====================================
        # NO DOCUMENT CONTEXT
        # =====================================

        if result is None:

            return StageResult(

                success=True,

                message=(
                    "No active document"
                ),

            )

        # =====================================
        # STORE SPECIALIZED RESPONSE
        # =====================================

        context.response = result

        # =====================================
        # STOP GENERAL PIPELINE
        # =====================================

        return StageResult(

            success=True,

            message=(
                "Document analysis completed"
            ),

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