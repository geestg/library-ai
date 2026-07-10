from app.rag.thesis_hybrid_search import (
    hybrid_search
)

from app.rag.reranker import (
    rerank
)

from app.services.research.query_normalizer import (
    normalize_research_query
)

from app.services.research.thesis_evidence_extractor import (
    extract_thesis_evidence
)

from app.services.research.diversity_filter import (
    apply_diversity_filter
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# BUILD THESIS OBJECT
# =====================================

def build_thesis_object(
    item: dict
):

    payload = item.get(
        "payload",
        {}
    )

    thesis = {

        "score":
        item.get(
            "rerank_score",
            0
        ),

        "title":
        payload.get("title"),

        "author":
        payload.get("author"),

        "year":
        payload.get("year"),

        "prodi":
        payload.get("prodi"),

        "abstract":
        payload.get("abstract"),

        "chunk":
        payload.get("chunk"),

        "url":
        payload.get("url")
    }

    thesis.update(

        extract_thesis_evidence(
            thesis
        )

    )

    return thesis


# =====================================
# BUILD CITATIONS
# =====================================

def build_citations(
    theses: list
):

    citations = []

    for idx, thesis in enumerate(
        theses,
        start=1
    ):

        citations.append({

            "source_id":
            idx,

            "title":
            thesis.get("title"),

            "author":
            thesis.get("author"),

            "year":
            thesis.get("year"),

            "prodi":
            thesis.get("prodi"),

            "url":
            thesis.get("url"),

            "score":
            thesis.get(
                "score",
                0
            ),

            "abstract":
            thesis.get(
                "abstract"
            ),

            "chunk":
            thesis.get(
                "chunk"
            ),

            "technologies":
            thesis.get(
                "technologies",
                []
            ),

            "methodologies":
            thesis.get(
                "methodologies",
                []
            ),

            "datasets":
            thesis.get(
                "datasets",
                []
            ),

            "evaluation_metrics":
            thesis.get(
                "evaluation_metrics",
                []
            )
        })

    return citations


# =====================================
# SEARCH PIPELINE
# =====================================

def run_search_pipeline(
    context: ResearchContext
):

    # =================================
    # RESOLVE EFFECTIVE QUERY
    # =================================

    effective_query = (

        context.resolved_query

        or

        context.query

    )

    # =================================
    # NORMALIZE QUERY
    # =================================

    context.normalized_query = (
        normalize_research_query(
            effective_query
        )
    )

    print(
        "[SEARCH QUERY]",
        effective_query
    )

    print(
        "[NORMALIZED QUERY]",
        context.normalized_query
    )

    # =================================
    # HYBRID SEARCH
    # =================================

    hybrid_results = hybrid_search(
        query=context.normalized_query,
        limit=50
    )

    # =================================
    # RERANK
    # =================================

    reranked_results = rerank(
        query=effective_query,
        documents=hybrid_results,
        top_k=20
    )

    print(
        f"[RERANK] {len(reranked_results)} results"
    )

    # =================================
    # FILTER
    # =================================

    filtered_results = [

        item

        for item in reranked_results

        if item.get(
            "rerank_score",
            0
        ) > 0
    ]

    print(
        f"[FILTERED] {len(filtered_results)} results"
    )

    # =================================
    # BUILD THESIS
    # =================================

    theses = [

        build_thesis_object(
            item
        )

        for item

        in filtered_results
    ]

    theses = apply_diversity_filter(

        theses,

        max_per_year=2,

        max_per_title_keyword=2
    )

    context.theses = (
        theses[:context.top_k]
    )

    context.citations = (
        build_citations(
            context.theses
        )
    )

    return context