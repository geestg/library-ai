from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import json

from app.services.research.research_engine import (
    research_analysis,
)

from app.services.research.serializers import (
    serialize_research_context,
)


router = APIRouter()


# =========================================
# STREAM EVENT
# =========================================

def stream_event(
    event_type: str,
    data,
):

    return (

        json.dumps(

            {

                "type": event_type,

                "data": data,

            },

            ensure_ascii=False,

        )

        + "\n"

    )


# =========================================
# REQUEST MODEL
# =========================================

class StreamRequest(BaseModel):

    session_id: str | None = None

    message: str

    active_document_ids: list = []


# =========================================
# STREAM CHAT
# =========================================

@router.post("/chat-stream")
def chat_stream(
    req: StreamRequest,
):

    def generate():

        try:

            # =====================================
            # START
            # =====================================

            yield stream_event(

                "start",

                {

                    "status":
                        "thinking",

                },

            )

            # =====================================
            # RESEARCH PIPELINE
            # =====================================

            context, llm_stream = (
                research_analysis(

                    session_id=(
                        req.session_id or ""
                    ),

                    query=req.message,

                    active_document_ids=(
                        req.active_document_ids
                    ),

                    stream=True,

                )
            )

            # =====================================
            # METADATA
            # =====================================

            yield stream_event(

                "metadata",

                {

                    "provider":
                        context.provider,

                    "model":
                        context.model,

                    "intent":
                        context.intent,

                },

            )

            # =====================================
            # SPECIALIZED RESPONSE
            # =====================================

            if context.response is not None:

                specialized_response = (
                    context.response
                )

                yield stream_event(

                    "context",

                    specialized_response,

                )

                analysis = (
                    specialized_response.get(
                        "analysis",
                        "",
                    )
                )

                if analysis:

                    yield stream_event(

                        "token",

                        analysis,

                    )

                yield stream_event(

                    "context_final",

                    specialized_response,

                )

                yield stream_event(

                    "end",

                    {

                        "status":
                            "completed",

                    },

                )

                return

            # =====================================
            # INITIAL CONTEXT
            # =====================================

            initial_context = (
                serialize_research_context(
                    context
                )
            )

            yield stream_event(

                "context",

                initial_context,

            )

            # =====================================
            # STREAM VALIDATION
            # =====================================

            if llm_stream is None:

                raise RuntimeError(

                    "Research pipeline completed "
                    "without a response or LLM stream."

                )

            # =====================================
            # TOKEN STREAM
            # =====================================

            analysis_chunks = []

            for token in llm_stream:

                analysis_chunks.append(
                    token
                )

                yield stream_event(

                    "token",

                    token,

                )

            # =====================================
            # FINAL ANALYSIS
            # =====================================

            context.analysis = "".join(
                analysis_chunks
            )

            # =====================================
            # FINAL CONTEXT
            # =====================================

            final_context = (
                serialize_research_context(
                    context
                )
            )

            yield stream_event(

                "context_final",

                final_context,

            )

            # =====================================
            # END
            # =====================================

            yield stream_event(

                "end",

                {

                    "status":
                        "completed",

                },

            )

        except Exception as exc:

            yield stream_event(

                "error",

                {

                    "status":
                        "failed",

                    "message":
                        str(exc),

                    "exception_type":
                        type(exc).__name__,

                },

            )

    return StreamingResponse(

        generate(),

        media_type="application/x-ndjson",

    )