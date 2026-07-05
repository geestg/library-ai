from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.pipeline import (
    ResearchPipelineBuilder,
)


# =====================================
# RESEARCH ANALYSIS ENGINE
# =====================================

def research_analysis(
    query: str,
    session_id: str = "",
    top_k: int = 10,
    mode: str = "analysis",
    active_document_ids=None,
    stream: bool = False,
):

    print("\n====================================")
    print("RESEARCH ENGINE V6")
    print("====================================")

    # =====================================
    # BUILD CONTEXT
    # =====================================

    context = ResearchContext(

        query=query,

        session_id=session_id,

        top_k=top_k,

        mode=mode,

        active_document_ids=(
            active_document_ids or []
        ),

    )

    # =====================================
    # ROUTING
    # =====================================

    from app.orchestration.task_router import (
        route_query,
    )

    routing = route_query(query)

    context.intent = routing.get(
        "intent",
        "",
    )

    context.provider = routing.get(
        "provider",
        "",
    )

    context.model = routing.get(
        "model",
        "",
    )

    # =====================================
    # BUILD & RUN PIPELINE
    # =====================================

    executor = (
        ResearchPipelineBuilder.build(
            context,
            stream=stream,
        )
    )

    executor.run()

    # =====================================
    # STREAM RESPONSE
    # =====================================

    if stream:

        return (

            context,

            context.llm_stream,

        )

    # =====================================
    # RESPONSE
    # =====================================

    return context.response