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
        # RESOLVE EFFECTIVE QUERY
        # =====================================

        effective_query = (

            context.resolved_query

            or

            context.query

        )

        # =====================================
        # RUNTIME QUERY TRACE
        # =====================================

        print(

            "[DOCUMENT QUERY]",

            {

                "original_query":
                    context.query,

                "effective_query":
                    effective_query,

                "query_was_resolved":
                    context.query_was_resolved,

            },

            flush=True,

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

            query=effective_query,

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

        citation_chunks = result.get(

            "citation_chunks",

            retrieved_chunks,

        )

        context.citations = (
            citation_chunks
        )

        context.evidence = {

            "retrieved_chunks":
                retrieved_chunks,

        }

        # =====================================
        # RESOLVE RESPONSE TYPE
        # =====================================

        response_type = result.get(
            "response_type"
        )

        # =====================================
        # STATIC RESPONSE
        # =====================================

        if response_type == "static":

            context.response = result

            context.llm_stream = None

            return StageResult(

                success=True,

                message=(
                    "Document static response prepared"
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

                    "citations":
                        len(
                            citation_chunks
                        ),

                    "stream":
                        False,

                    "answerability":
                        result.get(
                            "answerability"
                        ),

                    "response_type":
                        "static",

                    "query_was_resolved":
                        context.query_was_resolved,

                },

                stop_pipeline=True,

            )

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

                    "citations":
                        len(
                            citation_chunks
                        ),

                    "stream":
                        True,

                    "answerability":
                        result.get(
                            "answerability"
                        ),

                    "response_type":
                        "stream",

                    "query_was_resolved":
                        context.query_was_resolved,

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

                "citations":
                    len(
                        citation_chunks
                    ),

                "stream":
                    False,

                "answerability":
                    result.get(
                        "answerability"
                    ),

                "response_type":
                    response_type,

                "query_was_resolved":
                    context.query_was_resolved,

            },

            stop_pipeline=True,

        )

