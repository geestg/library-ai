from app.rag.thesis_hybrid_search import (
    hybrid_search
)

from app.rag.reranker import (
    rerank
)

from app.rag.context_synthesizer import (
    build_citation_context
)

from app.services.llm.model_gateway import (
    gateway
)

from app.services.research.evidence_extractor import (
    extract_evidence
)

from app.services.research.evidence_matrix import (
    build_evidence_matrix
)

from app.services.research.gap_detector import (
    detect_research_gaps
)

from app.services.research.prompt_builder import (
    build_evidence_section,
    build_matrix_section,
    build_research_prompt
)


# =====================================
# RESEARCH ANALYSIS ENGINE
# =====================================

def research_analysis(
    query: str,
    top_k: int = 10,
    mode: str = "analysis"
):

    print("\n====================================")
    print("RESEARCH ENGINE V3")
    print("====================================")

    # =================================
    # HYBRID SEARCH
    # =================================

    hybrid_results = hybrid_search(
        query=query,
        limit=50
    )

    print(
        f"[HYBRID SEARCH] {len(hybrid_results)} results"
    )

    # =================================
    # RERANK
    # =================================

    reranked_results = rerank(
        query=query,
        documents=hybrid_results,
        top_k=20
    )

    print(
        f"[RERANK] {len(reranked_results)} results"
    )

    # =================================
    # FILTER POSITIVE SCORES
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
    # NORMALIZE THESIS
    # =================================

    theses = []

    for item in filtered_results:

        payload = item.get(
            "payload",
            {}
        )

        theses.append({

            "score":
            item.get(
                "rerank_score",
                0
            ),

            "title":
            payload.get(
                "title"
            ),

            "author":
            payload.get(
                "author"
            ),

            "year":
            payload.get(
                "year"
            ),

            "prodi":
            payload.get(
                "prodi"
            ),

            "abstract":
            payload.get(
                "abstract"
            ),

            "chunk":
            payload.get(
                "chunk"
            ),

            "url":
            payload.get(
                "url"
            )
        })

    theses = theses[:top_k]

    # =================================
    # DEBUG THESIS
    # =================================

    print("\n====================================")
    print("TOP THESIS")
    print("====================================")

    for idx, thesis in enumerate(
        theses,
        start=1
    ):

        print(
            f"{idx}. "
            f"{thesis.get('title', '-')}"
        )

        print(
            f"Score: "
            f"{thesis.get('score', 0):.4f}"
        )

    # =================================
    # EVIDENCE EXTRACTION
    # =================================

    evidence = extract_evidence(
        theses
    )

    print("\n====================================")
    print("STRUCTURED EVIDENCE")
    print("====================================")

    print(
        evidence
    )

    # =================================
    # EVIDENCE MATRIX
    # =================================

    evidence_matrix = (
        build_evidence_matrix(
            evidence
        )
    )

    print("\n====================================")
    print("EVIDENCE MATRIX")
    print("====================================")

    print(
        evidence_matrix
    )

    # =================================
    # GAP ANALYSIS
    # =================================

    gap_analysis = (
        detect_research_gaps(
            evidence_matrix
        )
    )

    print("\n====================================")
    print("GAP ANALYSIS")
    print("====================================")

    print(
        gap_analysis
    )

    # =================================
    # EVIDENCE TEXT
    # =================================

    evidence_text = (
        build_evidence_section(
            evidence
        )
    )

    matrix_text = (
        build_matrix_section(
            evidence_matrix
        )
    )

    combined_evidence = (

        evidence_text

        + "\n\n"

        + matrix_text

        + "\n\n"

        + "GAP ANALYSIS\n"
        + "=" * 50
        + "\n"
        + str(gap_analysis)
    )

    # =================================
    # CITATION CONTEXT
    # =================================

    citation_results = []

    for thesis in theses:

        citation_results.append({

            "payload":
            thesis,

            "score":
            thesis.get(
                "score",
                0
            )
        })

    citation_context = (
        build_citation_context(
            citation_results
        )
    )

    # =================================
    # CITATIONS
    # =================================

    citations = []

    for idx, thesis in enumerate(
        theses,
        start=1
    ):

        citations.append({

            "source_id":
            idx,

            "title":
            thesis.get(
                "title"
            ),

            "author":
            thesis.get(
                "author"
            ),

            "year":
            thesis.get(
                "year"
            ),

            "prodi":
            thesis.get(
                "prodi"
            ),

            "url":
            thesis.get(
                "url"
            ),

            "score":
            thesis.get(
                "score",
                0
            )
        })

    # =================================
    # PROMPT
    # =================================

    prompt = build_research_prompt(

        query=query,

        evidence_text=
        combined_evidence,

        citation_context=
        citation_context,

        mode=mode
    )

    print("\n====================================")
    print("PROMPT GENERATED")
    print("====================================")

    # =================================
    # LLM
    # =================================

    analysis = gateway.generate_response(
        prompt=prompt
    )

    # =================================
    # RETURN
    # =================================

    return {

        "query":
        query,

        "mode":
        mode,

        "related_theses":
        theses,

        "citations":
        citations,

        "evidence":
        evidence,

        "evidence_matrix":
        evidence_matrix,

        "gap_analysis":
        gap_analysis,

        "analysis":
        analysis
    }