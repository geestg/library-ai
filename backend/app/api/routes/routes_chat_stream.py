from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import json
import re

from app.services.research.research_engine import (
    persist_assistant_response,
    persist_execution_snapshot,
)

from app.services.research.agents import ResearchAgent
from app.services.research.research_engine import (
    serialize_research_context,
)

from app.services.research.session import (
    session_manager,
)

# =========================================
# LIBRARY PIPELINE IMPORTS
# =========================================

from app.orchestration.intent_classifier import (
    classify_intent,
)

from app.orchestration.model_selector import (
    select_model,
)

from app.rag.library_search import (
    library_hybrid_search,
)

from app.rag.reranker import (
    rerank,
)

from app.rag.library_context_builder import (
    build_library_book_context,
)

from app.services.prompt.prompt_builder import (
    build_prompt,
)

from app.services.llm.model_gateway import (
    gateway,
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
# PERSIST STREAM ASSISTANT
# =========================================

def persist_stream_assistant(
    context,
    response,
) -> str:
    session = session_manager.get(
        context.session_id
    )
    if session is None:
        return ""
    return persist_assistant_response(
        session=session,
        response=response,
    )


# =========================================
# PERSIST STREAM EXECUTION
# =========================================

def persist_stream_execution(
    context,
    response_content: str = "",
) -> dict:
    session = session_manager.get(
        context.session_id
    )
    if session is None:
        return {}
    return persist_execution_snapshot(
        session=session,
        context=context,
        response_content=(
            response_content
        ),
    )


# =========================================
# REQUEST MODEL
# =========================================

class StreamRequest(BaseModel):
    session_id: str | None = None
    message: str
    active_document_ids: list = []


# =========================================
# LIBRARY PIPELINE HANDLER
# =========================================

def _run_library_pipeline(req, intent: str):
    """
    Pipeline khusus rekomendasi buku perpustakaan.
    Menggunakan library_books collection di Qdrant.
    Dipanggil oleh generate() saat intent == 'recommendation'.
    """

    selected = select_model(intent)
    provider = selected["provider"]
    model    = selected["model"]

    yield stream_event(
        "metadata",
        {"provider": provider, "model": model, "intent": intent},
    )

    # Clean conversational noise from search query (e.g. "Di mana lokasi rak untuk buku...")
    noise_patterns = [
        r"(?i)^di\s+mana\s+lokasi\s+rak\s+untuk\s+buku\s+",
        r"(?i)^di\s+mana\s+lokasi\s+rak\s+buku\s+",
        r"(?i)^di\s+mana\s+lokasi\s+buku\s+",
        r"(?i)^lokasi\s+rak\s+buku\s+",
        r"(?i)^cari\s+buku\s+tentang\s+",
        r"(?i)^buku\s+tentang\s+",
        r"(?i)^rekomendasi\s+buku\s+",
        r"(?i)^buku\s+apa\s+yang\s+",
        r"(?i)^bisa\s+carikan\s+buku\s+",
    ]
    clean_query = req.message.strip()
    for pattern in noise_patterns:
        clean_query = re.sub(pattern, "", clean_query)
    clean_query = clean_query.strip(" ?!.")
    # Bilingual Query Expansion (Comprehensive IT Del Institutional Academic Dictionary)
    bilingual_terms = {
        # FITE & Vokasi (SI, IF, TI, TRPL, TK, D3 TI)
        "struktur data": "data structures",
        "algoritma": "algorithms",
        "sistem operasi": "operating systems",
        "jaringan komputer": "computer networking",
        "basis data": "database systems",
        "kecerdasan buatan": "artificial intelligence",
        "pembelajaran mesin": "machine learning",
        "pembelajaran mendalam": "deep learning",
        "rekayasa perangkat lunak": "software engineering",
        "pemrograman web": "web programming",
        "pemrograman terstruktur": "structured programming",
        "pemrograman berorientasi objek": "object oriented programming",
        "keamanan siber": "cybersecurity",
        "keamanan jaringan": "network security",
        "sistem tertanam": "embedded systems",
        "pengolahan citra": "image processing",
        "visi komputer": "computer vision",
        "pemrosesan bahasa alami": "natural language processing",
        "analisis data": "data analytics",
        "sains data": "data science",
        "penambangan data": "data mining",
        "sistem pakar": "expert systems",
        "interaksi manusia komputer": "human computer interaction",
        "komputasi awan": "cloud computing",
        "sistem terdistribusi": "distributed systems",
        "sistem informasi manajemen": "management information systems",

        # Teknik Elektro (FITE - TE)
        "teknik elektro": "electrical engineering",
        "rangkaian listrik": "electric circuits",
        "sistem kendali": "control systems",
        "pemrosesan sinyal": "signal processing",
        "mikrokontroler": "microcontrollers",
        "elektronika analog": "analog electronics",
        "elektronika digital": "digital electronics",
        "telekomunikasi": "telecommunications",
        "sistem tenaga listrik": "power systems",
        "sensor dan aktuator": "sensors and actuators",

        # FTI (Manajemen Rekayasa, Teknik Metalurgi)
        "manajemen rekayasa": "engineering management",
        "rantai pasok": "supply chain",
        "logistik": "logistics",
        "manajemen operasi": "operations management",
        "manajemen proyek": "project management",
        "manajemen kualitas": "quality management",
        "manufaktur cerdas": "smart manufacturing",
        "teknik metalurgi": "metallurgical engineering",
        "ekstraksi logam": "extractive metallurgy",
        "ilmu bahan": "materials science",
        "korosi": "corrosion",
        "rekayasa proses": "process engineering",
        "penelitian operasional": "operations research",

        # Bioteknologi & Bioproses (FITE - Biotek / TB)
        "bioteknologi": "biotechnology",
        "teknik bioproses": "bioprocess engineering",
        "biologi molekuler": "molecular biology",
        "rekayasa genetika": "genetic engineering",
        "bioinformatika": "bioinformatics",
        "mikrobiologi": "microbiology",
        "biokimia": "biochemistry",
        "fermentasi": "fermentation",
        "teknologi enzim": "enzyme technology",
        "kultur jaringan": "tissue culture"
    }

    expanded_terms = []
    clean_lower = clean_query.lower()
    for id_term, en_term in bilingual_terms.items():
        if id_term in clean_lower and en_term not in clean_lower:
            expanded_terms.append(en_term)

    # search_term: bilingual (for Qdrant hybrid search - vector + BM25)
    # rerank_query: English-ONLY (for ms-marco Cross-Encoder which is English-only trained)
    #   Using English terms ensures cross-encoder correctly ranks
    #   'Introduction to Algorithms' above 'Algoritma dan Pemrograman PHP'
    if expanded_terms:
        search_term  = f"{clean_query} {' '.join(expanded_terms)}"
        rerank_query = ' '.join(expanded_terms)  # English only → correct cross-encoder scoring
    else:
        # If no expansion (query already in English), use clean_query for both
        search_term  = clean_query
        rerank_query = clean_query
    print(f"[LIBRARY SEARCH] Raw: '{req.message}' -> Clean: '{clean_query}' -> English Search: '{rerank_query}'")

    # Use English-only query for ALL three components:
    # - nomic-embed (vector) is cross-lingual: "data structures algorithms" already
    #   retrieves Indonesian books like "Konsep Struktur Data dengan C++" semantically.
    # - Including Indonesian words ("algoritma") in vector query pulls wrong books
    #   like "Data Mining Algoritma PHP" into the candidate pool unnecessarily.
    # - BM25 and Reranker (ms-marco) are English-only by design.
    raw_results = library_hybrid_search(rerank_query, limit=20, bm25_query=rerank_query)

    documents = []
    for r in raw_results:
        payload = r.get("payload", {})
        documents.append({
            "text":    payload.get("text", ""),
            "payload": payload,
            "score":   r.get("score", 0),
        })

    # Rerank with English-only query so cross-encoder (ms-marco) correctly
    # scores English-titled books higher than false positives
    ranked_docs = rerank(rerank_query, documents)
    top_docs    = ranked_docs[:5]

    # Confidence Threshold Check (Prevent forced hallucinated recommendations)
    max_score = max([doc.get("rerank_score", -999) for doc in top_docs]) if top_docs else -999
    print(f"[LIBRARY CONFIDENCE] Max Rerank Score: {max_score:.4f}")

    if max_score < -1.0:
        context = "STATUS: RELEVANSI RENDAH (TIDAK DITEMUKAN BUKU SPESIFIK TEPAT DI KATALOG).\n" + build_library_book_context(top_docs[:3])
    else:
        context = build_library_book_context(top_docs)

    prompt = build_prompt(
        query=req.message,
        context=context,
        intent=intent,
    )

    llm_stream = gateway.stream_response(
        prompt=prompt,
        model=model,
        provider=provider,
    )

    if llm_stream is None:
        yield stream_event("error", {"message": "LLM stream gagal"})
        yield stream_event("end", {"status": "failed"})
        return

    for token in llm_stream:
        yield stream_event("token", token)

    sources = []
    for idx, doc in enumerate(top_docs, start=1):
        payload = doc.get("payload", {})
        sources.append({
            "source_id": idx,
            "title":     payload.get("title", "-"),
            "author":    payload.get("author", payload.get("penulis", "-")),
            "subject":   payload.get("subject", payload.get("subjek", "-")),
            "location":  payload.get("location", payload.get("lokasi", "-")),
            "score":     round(doc.get("rerank_score", 0), 4),
        })

    yield stream_event("context_final", {"sources": sources})
    yield stream_event("end", {"status": "completed"})


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
            # INTENT DETECTION
            # =====================================
            intent = classify_intent(req.message)
            print(f"\n[STREAM INTENT] {intent}")

            # =====================================
            # LIBRARY PIPELINE (recommendation)
            # =====================================
            if intent == "recommendation":
                yield from _run_library_pipeline(
                    req=req,
                    intent=intent,
                )
                return

            # =====================================
            # RESEARCH PIPELINE (semua intent lain)
            # =====================================
            agent = ResearchAgent()
            context, llm_stream = agent.run(
                query=req.message,
                session_id=req.session_id or "",
                active_document_ids=req.active_document_ids,
                stream=True,
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
                specialized_response = context.response
                yield stream_event(
                    "context",
                    specialized_response,
                )
                if isinstance(specialized_response, str):
                    analysis = specialized_response
                elif isinstance(specialized_response, dict):
                    analysis = (
                        specialized_response.get("ideas")
                        or specialized_response.get("analysis")
                        or specialized_response.get("literature_review")
                        or specialized_response.get("gap_report")
                        or specialized_response.get("novelty_check")
                        or specialized_response.get("method_comparison")
                        or specialized_response.get("detail_explanation")
                        or ""
                    )
                else:
                    analysis = str(specialized_response)

                if analysis:
                    yield stream_event(
                        "token",
                        analysis,
                    )

                # =================================
                # PERSIST SPECIALIZED ASSISTANT
                # =================================
                assistant_content = (
                    persist_stream_assistant(
                        context=context,
                        response=(
                            specialized_response
                        ),
                    )
                )

                # =================================
                # PERSIST SPECIALIZED EXECUTION
                # =================================
                persist_stream_execution(
                    context=context,
                    response_content=(
                        assistant_content
                    ),
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
            # PERSIST STREAMED ASSISTANT
            # =====================================
            assistant_content = (
                persist_stream_assistant(
                    context=context,
                    response={
                        "analysis":
                            context.analysis,
                    },
                )
            )

            # =====================================
            # PERSIST STREAMED EXECUTION
            # =====================================
            persist_stream_execution(
                context=context,
                response_content=(
                    assistant_content
                ),
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