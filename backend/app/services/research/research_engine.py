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

from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
)

from app.services.research.method_comparison_engine import (
    is_comparison_query,
    run_method_comparison
)

from app.services.research.novelty_scorer import (
    calculate_novelty_score
)

from app.services.research.thesis_idea_generator import (
    generate_thesis_ideas
)

from app.services.research.literature_review_generator import (
    generate_literature_review
)

from app.services.research.intent_detector import (
    is_literature_review_query,
    is_thesis_idea_query
)

from app.services.research.query_normalizer import (
    normalize_research_query
)

# =====================================
# RESEARCH ANALYSIS ENGINE
# =====================================

def research_analysis(
    query: str,
    top_k: int = 10,
    mode: str = "analysis",
    active_document_ids=None
):

    print("\n====================================")
    print("RESEARCH ENGINE V3")
    print("====================================")
    
    # =================================
    # ACTIVE DOCUMENT MODE
    # =================================

    if active_document_ids:

        contexts = []

        documents = []

        for doc_id in active_document_ids:

            doc = ACTIVE_DOCUMENTS.get(
                doc_id
            )

            if not doc:
                continue

            documents.append({

                "document_id":
                doc_id,

                "filename":
                doc["filename"]

            })

            contexts.append(

                f"""
    FILE:
    {doc["filename"]}

    CONTENT:
    {doc["content"][:10000]}
    """
            )

        if contexts:

            document_context = "\n\n".join(
                contexts
            )

            prompt = f"""
    Anda adalah DELBot.

    Anda sedang menganalisis
    beberapa dokumen sekaligus.

    ==================================================
    DOKUMEN
    ==================================================

    {document_context}

    ==================================================
    PERTANYAAN USER
    ==================================================

    {query}

    ==================================================
    ATURAN
    ==================================================

    1. Jawab berdasarkan dokumen yang diberikan.

    2. Jika informasi berasal dari dokumen tertentu,
    sebutkan nama filenya.

    3. Jika terdapat informasi yang berbeda antar dokumen,
    jelaskan perbedaannya.

    4. Jika user meminta perbandingan,
    buat tabel perbandingan.

    5. Jika user meminta ringkasan,
    buat ringkasan terstruktur.

    6. Jika informasi tidak ditemukan,
    katakan informasi tidak ditemukan.

    7. Jangan gunakan Qdrant.

    8. Jangan gunakan repository skripsi.

    9. Jangan mengarang.

    10. Gunakan Bahasa Indonesia.
    """

            answer = (
                gateway.generate_response(
                    prompt=prompt
                )
            )

            return {

                "query":
                query,

                "mode":
                "multi_document",

                "analysis":
                answer,

                "citations":
                [],

                "evidence":
                {},

                "documents":
                documents

            }
       
    # =================================
    # HYBRID SEARCH
    # =================================

    normalized_query = (
        normalize_research_query(
            query
        )
    )

    print(
        "[NORMALIZED QUERY]",
        normalized_query
    )

    hybrid_results = hybrid_search(
        query=normalized_query,
        limit=50
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
    # CITATIONS
    # =================================

    citations = []

    for idx, thesis in enumerate(
        theses,
        start=1
    ):

        citations.append({

            "source_id": idx,
            "title": thesis.get("title"),
            "author": thesis.get("author"),
            "year": thesis.get("year"),
            "prodi": thesis.get("prodi"),
            "url": thesis.get("url"),
            "score": thesis.get("score", 0),
            "abstract": thesis.get("abstract"),
            "chunk": thesis.get("chunk")
        })

    # =================================
    # METHOD COMPARISON MODE
    # =================================

    if is_comparison_query(query):

        print("\n====================================")
        print("METHOD COMPARISON MODE")
        print("====================================")

        comparison_result = (
            run_method_comparison(
                query=query,
                theses=theses
            )
        )


        return {

            "query":
            query,

            "mode":
            "comparison",

            "related_theses":
            theses,

            "citations":
            citations,

            "comparison_matrix":
            comparison_result.get(
                "comparison_matrix",
                {}
            ),

            "comparison":
            comparison_result.get(
                "comparison",
                ""
            ),

            "analysis":
            comparison_result.get(
                "comparison",
                ""
            )
        }

    # =================================
    # TOP THESIS DEBUG
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
    # THESIS CONTENT DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("THESIS DEBUG")
    print("=" * 80)

    for idx, thesis in enumerate(
        theses,
        start=1
    ):

        print(
            f"\n[{idx}] "
            f"{thesis.get('title')}"
        )

        abstract = (
            thesis.get(
                "abstract",
                ""
            ) or ""
        )

        print(
            abstract[:500]
        )

    # =================================
    # EVIDENCE EXTRACTION
    # =================================

    evidence = extract_evidence(
        theses
    )

    # =================================
    # EVIDENCE DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("EVIDENCE DEBUG")
    print("=" * 80)

    print(evidence)

    print("\nTECHNOLOGIES")
    print(

        evidence.get(
            "technologies",
            []
        )
    )

    print("\nMETHODS")
    print(

        evidence.get(
            "methodologies",
            []
        )
    )

    print("\nDOMAINS")
    print(

        evidence.get(
            "research_domains",
            []
        )
    )

    # =================================
    # STRUCTURED EVIDENCE
    # =================================

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

    # =================================
    # NOVELTY ANALYSIS
    # =================================

    novelty_analysis = (
        calculate_novelty_score(
            evidence_matrix,
            gap_analysis
        )
    )

    if is_thesis_idea_query(query):

        idea_result = (
            generate_thesis_ideas(

                query=query,

                evidence=evidence,

                evidence_matrix=evidence_matrix,

                gap_analysis=gap_analysis,

                novelty_analysis=novelty_analysis
            )
        )

        return {

            "query":
            query,

            "mode":
            "thesis_ideas",

            "analysis":
            idea_result["ideas"],

            "citations":
            citations,

            "evidence":
            evidence,

            "evidence_matrix":
            evidence_matrix,

            "gap_analysis":
            gap_analysis,

            "novelty_analysis":
            novelty_analysis
        }

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

    if is_literature_review_query(
        query
    ):

        review_result = (
            generate_literature_review(

                query=query,

                evidence=evidence,

                evidence_matrix=evidence_matrix,

                gap_analysis=gap_analysis,

                citation_context=citation_context
            )
        )

        return {

            "query":
            query,

            "mode":
            "literature_review",

            "analysis":
            review_result[
                "literature_review"
            ],

            "citations":
            citations,

            "evidence":
            evidence,

            "evidence_matrix":
            evidence_matrix,

            "gap_analysis":
            gap_analysis
        }

    
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

    # =====================================
    # RETURN
    # =====================================

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

        "novelty_analysis":
        novelty_analysis,

        "analysis":
        analysis
    }