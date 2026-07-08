from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.pipeline import (
    ResearchPipelineBuilder,
)

from app.services.research.serializers import (
    serialize_research_context,
)

from app.services.research.session import (
    session_manager,
)


# =====================================
# EXTRACT ASSISTANT CONTENT
# =====================================

def extract_assistant_content(
    response,
) -> str:

    if not isinstance(
        response,
        dict,
    ):

        return ""

    candidates = [

        response.get(
            "analysis"
        ),

        response.get(
            "answer"
        ),

        response.get(
            "comparison"
        ),

    ]

    for content in candidates:

        if (
            isinstance(content, str)
            and content.strip()
        ):

            return content.strip()

    return ""


# =====================================
# PERSIST ASSISTANT RESPONSE
# =====================================

def persist_assistant_response(
    session,
    response,
) -> str:

    assistant_content = (
        extract_assistant_content(
            response
        )
    )

    if not assistant_content:

        return ""

    session.conversation.append(

        role="assistant",

        content=assistant_content,

    )

    return assistant_content


# =====================================
# PERSIST EXECUTION SNAPSHOT
# =====================================

def persist_execution_snapshot(
    session,
    context: ResearchContext,
    response_content: str = "",
) -> dict:

    serialized_context = (
        serialize_research_context(
            context
        )
    )

    session.execution.update(

        context=context,

        serialized_context=(
            serialized_context
        ),

        response_content=(
            response_content
        ),

    )

    return serialized_context


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
    progress_callback=None,
):

    print("\n====================================")
    print("RESEARCH ENGINE V6")
    print("====================================")

    # =====================================
    # RESOLVE SESSION
    # =====================================

    session = session_manager.get_or_create(
        session_id
    )

    # =====================================
    # SNAPSHOT PREVIOUS CONVERSATION
    # =====================================

    conversation_history = (
        session.conversation.build_history()
    )

    # =====================================
    # RECORD CURRENT USER MESSAGE
    # =====================================

    session.conversation.append(

        role="user",

        content=query,

    )

    # =====================================
    # BUILD CONTEXT
    # =====================================

    context = ResearchContext(

        query=query,

        session_id=session.session_id,

        top_k=top_k,

        mode=mode,

        active_document_ids=(
            active_document_ids or []
        ),

        conversation_history=(
            conversation_history
        ),

    )

    # =====================================
    # ROUTING
    # =====================================

    from app.orchestration.task_router import (
        route_query,
    )

    routing = route_query(
        query
    )

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

            progress_callback=(
                progress_callback
            ),

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
    # PERSIST ASSISTANT RESPONSE
    # =====================================

    assistant_content = (
        persist_assistant_response(

            session=session,

            response=context.response,

        )
    )

    # =====================================
    # PERSIST EXECUTION SNAPSHOT
    # =====================================

    persist_execution_snapshot(

        session=session,

        context=context,

        response_content=(
            assistant_content
        ),

    )

    # =====================================
    # RESPONSE
    # =====================================

    return context.response