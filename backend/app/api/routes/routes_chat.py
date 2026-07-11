from fastapi import APIRouter

from pydantic import BaseModel

from app.orchestration.task_router import (
    route_query,
)

from app.rag.hybrid_search import (
    hybrid_search,
)

from app.rag.reranker import (
    rerank,
)

from app.rag.context_synthesizer import (
    build_citation_context,
)

from app.rag.source_mapper import (
    build_source_map,
)

from app.services.llm.tasks.llm_task import (
    LLMTask,
)

from app.services.llm.prompts.models.prompt_request import (
    PromptRequest,
)

from app.services.prompt.prompt_builder import (
    build_prompt,
)

router = APIRouter()


# =========================================
# REQUEST MODEL
# =========================================

class ChatRequest(BaseModel):

    message: str


# =========================================
# CHAT ROUTE
# =========================================

@router.post("/chat")
def chat(req: ChatRequest):

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

        limit=15,

    )

    # =====================================
    # PREPARE DOCUMENTS
    # =====================================

    documents = []

    for r in results:

        payload = r.get(
            "payload",
            {},
        )

        documents.append({

            "text":
                payload.get(
                    "text",
                    "",
                ),

            "payload":
                payload,

            "score":
                r.get(
                    "score",
                    0,
                ),

        })

    # =====================================
    # RERANKING
    # =====================================

    ranked_docs = rerank(

        req.message,

        documents,

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

        intent=intent,

    )

    # =====================================
    # BUILD REQUEST
    # =====================================

    request = PromptRequest(

        prompt=prompt,

        model=selected_model,

        provider=selected_provider,

    )

    # =====================================
    # LLM GENERATION
    # =====================================

    response = LLMTask.answer(
        request
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

    for idx, r in enumerate(
        top_docs,
        start=1,
    ):

        payload = r.get(
            "payload",
            {},
        )

        sources.append({

            "source_id":
                idx,

            "source_file":
                payload.get(
                    "source_file",
                    "",
                ),

            "page":
                payload.get(
                    "page",
                    "",
                ),

            "chunk_index":
                payload.get(
                    "chunk_index",
                    "",
                ),

            "title":
                payload.get(
                    "title",
                    "",
                ),

            "score":
                r.get(
                    "rerank_score",
                    0,
                ),

        })

    # =====================================
    # FINAL RESPONSE
    # =====================================

    return {

        "status":
            "success",

        "intent":
            intent,

        "provider":
            selected_provider,

        "model":
            selected_model,

        "response":
            response,

        "citations":
            citations,

        "sources":
            sources,

    }