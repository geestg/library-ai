from app.services.research.pipeline.base_stage import (
    BaseStage,
)

from app.services.research.pipeline.stage_result import (
    StageResult,
)

from app.services.research.engines.query_resolution_engine import (
    resolve_query,
)


class QueryResolutionStage(
    BaseStage
):

    name = "query_resolution"

    def execute(
        self,
        context,
    ):

        # =====================================
        # RESOLVE QUERY
        # =====================================

        result = resolve_query(

            query=context.query,

            conversation_history=(
                context.conversation_history
            ),

            model=(
                context.model or None
            ),

            provider=(
                context.provider or None
            ),

        )

        # =====================================
        # STORE RESOLVED QUERY
        # =====================================

        context.resolved_query = (

            result.get(
                "resolved_query"
            )

            or

            context.query

        )

        # =====================================
        # STORE RESOLUTION STATE
        # =====================================

        context.query_was_resolved = bool(

            result.get(
                "was_resolved",
                False,
            )

        )

        # =====================================
        # RUNTIME TRACE
        # =====================================

        print(

            "[QUERY RESOLUTION]",

            {

                "query":
                    context.query,

                "resolved_query":
                    context.resolved_query,

                "was_resolved":
                    context.query_was_resolved,

                "reason":
                    result.get(
                        "reason"
                    ),

            },

            flush=True,

        )

        # =====================================
        # DONE
        # =====================================

        return StageResult(

            success=True,

            message=(

                "Query context resolved"

                if context.query_was_resolved

                else

                "Query resolution not required"

            ),

            metadata={

                "was_resolved":
                    context.query_was_resolved,

                "reason":
                    result.get(
                        "reason"
                    ),

            },

        )

