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

    def __init__(
        self,
        stream: bool = False,
    ):

        self.stream = stream

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

            model=(
                context.model or None
            ),

            provider=(
                context.provider or None
            ),

            stream=self.stream,

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
                    "No relevant document context"
                ),

            )

        # =====================================
        # STORE DOCUMENT EVIDENCE
        # =====================================

        retrieved_chunks = result.get(

            "retrieved_chunks",

            [],

        )

        context.citations = (
            retrieved_chunks
        )

        context.evidence = {

            "retrieved_chunks":
                retrieved_chunks,

        }

        # =====================================
        # STREAM MODE
        # =====================================

        if self.stream:

            llm_stream = result.get(
                "llm_stream"
            )

            if llm_stream is None:

                raise RuntimeError(

                    "Document analysis did not "
                    "return an LLM stream."

                )

            # =================================
            # STORE STREAM
            # =================================

            context.llm_stream = (
                llm_stream
            )

            # =================================
            # KEEP RESPONSE EMPTY
            # =================================

            context.response = None

            return StageResult(

                success=True,

                message=(
                    "Document stream prepared"
                ),

                metadata={

                    "documents":
                        len(

                            result.get(

                                "documents",

                                [],

                            )

                        ),

                    "retrieved_chunks":
                        len(
                            retrieved_chunks
                        ),

                    "stream":
                        True,

                },

                stop_pipeline=True,

            )

        # =====================================
        # NORMAL MODE
        # =====================================

        context.response = result

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

                "retrieved_chunks":
                    len(
                        retrieved_chunks
                    ),

                "stream":
                    False,

            },

            stop_pipeline=True,

        )