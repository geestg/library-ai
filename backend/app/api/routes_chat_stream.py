from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from pydantic import BaseModel

import json

from app.orchestration.task_router import (
    route_query
)

from app.rag.hybrid_search import (
    hybrid_search
)

from app.rag.reranker import (
    rerank
)

from app.rag.context_synthesizer import (
    build_citation_context
)

from app.rag.source_mapper import (
    build_source_map
)

from app.services.llm.model_gateway import (
    gateway
)

from app.services.prompt.prompt_builder import (
    build_prompt
)

router = APIRouter()


# =========================================
# REQUEST MODEL
# =========================================

class StreamRequest(BaseModel):

    message: str


# =========================================
# STREAM CHAT ROUTE
# =========================================

@router.post("/chat-stream")
def chat_stream(req: StreamRequest):

    # =====================================
    # AI ORCHESTRATION
    # =====================================

    routing = route_query(
        req.message
    )

    intent = routing["intent"]

    selected_model = routing["model"]

    selected_provider = routing["provider"]

    # =====================================
    # HYBRID SEARCH
    # =====================================

    results = hybrid_search(

        req.message,

        limit=15
    )

    # =====================================
    # PREPARE DOCUMENTS
    # =====================================

    documents = []

    for r in results:

        payload = r.get(
            "payload",
            {}
        )

        text = payload.get(
            "text",
            ""
        )

        documents.append({

            "text": text,

            "payload": payload,

            "score": r.get(
                "score",
                0
            )
        })

    # =====================================
    # RERANKING
    # =====================================

    ranked_docs = rerank(

        req.message,

        documents
    )

    top_docs = ranked_docs[:5]

    # =====================================
    # CITATION CONTEXT
    # =====================================

    context = build_citation_context(
        top_docs
    )

    # =====================================
    # PROMPT BUILDING
    # =====================================

    prompt = build_prompt(

        query=req.message,

        context=context,

        intent=intent
    )

    # =====================================
    # STRUCTURED CITATIONS
    # =====================================

    citations = build_source_map(
        top_docs
    )

    # =====================================
    # SOURCES
    # =====================================

    sources = []

    for idx, r in enumerate(top_docs, start=1):

        payload = r.get(
            "payload",
            {}
        )

        sources.append({

            "source_id": idx,

            "source_file": payload.get(
                "source_file",
                ""
            ),

            "page": payload.get(
                "page",
                ""
            ),

            "chunk_index": payload.get(
                "chunk_index",
                ""
            ),

            "title": payload.get(
                "title",
                ""
            ),

            "score": r.get(
                "rerank_score",
                0
            )
        })

    # =====================================
    # STREAM GENERATOR
    # =====================================

    def generate():

        stream = gateway.stream_response(

            prompt=prompt,

            model=selected_model,

            provider=selected_provider
        )

        # =================================
        # TOKEN STREAM
        # =================================

        for chunk in stream:

            yield (
                json.dumps({
                    "type": "token",
                    "content": chunk
                }) + "\n"
            )

        # =================================
        # CITATIONS EVENT
        # =================================

        yield (
            json.dumps({
                "type": "citations",
                "data": citations
            }) + "\n"
        )

        # =================================
        # SOURCES EVENT
        # =================================

        yield (
            json.dumps({
                "type": "sources",
                "data": sources
            }) + "\n"
        )

    # =====================================
    # STREAM RESPONSE
    # =====================================

    return StreamingResponse(

        generate(),

        media_type="text/plain"
    )