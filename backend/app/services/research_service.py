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


# =====================================
# BUILD PROMPT BY MODE
# =====================================

def build_prompt_by_mode(

    mode: str,

    query: str,

    context: str

):

    # =================================
    # LITERATURE REVIEW
    # =================================

    if mode == "literature_review":

        return f"""
You are a senior academic researcher.

==================================================
TOPIC
==================================================

{query}

==================================================
RETRIEVED SOURCES
==================================================

{context}

==================================================
TASK
==================================================

Create a structured academic Literature Review.

==================================================
RULES
==================================================

- Use only retrieved sources
- Do not hallucinate
- Use citations [1], [2], [3]
- Compare studies
- Identify trends
- Identify limitations
- Identify research gaps

==================================================
OUTPUT
==================================================

# Introduction

# Previous Studies

# Research Trends

# Research Comparison

# Research Gaps

# Conclusion
"""

    # =================================
    # TITLE GENERATION
    # =================================

    if mode == "title_generation":

        return f"""
You are a senior thesis advisor.

==================================================
TOPIC
==================================================

{query}

==================================================
RETRIEVED SOURCES
==================================================

{context}

==================================================
TASK
==================================================

1. Identify research gaps
2. Identify weaknesses
3. Identify novelty opportunities
4. Generate 20 thesis title ideas

==================================================
RULES
==================================================

- Use only retrieved sources
- Do not hallucinate
- Use citations [1], [2], [3]
- Do not introduce unsupported technologies

==================================================
OUTPUT
==================================================

# Research Gaps

# Weaknesses

# Novelty Opportunities

# Thesis Title Ideas
"""

    # =================================
    # COMPARISON MATRIX
    # =================================

    if mode == "comparison_matrix":

        return f"""
You are a senior academic reviewer.

==================================================
TOPIC
==================================================

{query}

==================================================
RETRIEVED SOURCES
==================================================

{context}

==================================================
TASK
==================================================

Compare all retrieved studies.

==================================================
RULES
==================================================

- Use only retrieved sources
- Use citations [1], [2], [3]
- Do not hallucinate
- Do not invent methods
- Do not invent technologies
- Every comparison must be grounded
- If information is missing, write:
  "Not explicitly stated"

==================================================
OUTPUT
==================================================

# Research Comparison Matrix

| Study | Year | Methodology | Technology | Strengths | Weaknesses |

# Comparative Analysis

# Common Trends

# Research Gaps

# Recommendation
"""

    # =================================
    # DEFAULT ANALYSIS
    # =================================

    return f"""
You are a senior professor,
thesis examiner,
research supervisor,
and academic reviewer.

==================================================
RESEARCH TOPIC
==================================================

{query}

==================================================
RETRIEVED THESIS DATA
==================================================

{context}

==================================================
IMPORTANT RULES
==================================================

1. ONLY use information from the retrieved theses.

2. Every statement, recommendation,
technology, methodology, research gap,
future direction, and thesis title
MUST be traceable to the retrieved theses.

3. DO NOT invent:
- technologies
- frameworks
- methods
- architectures
- datasets
- research domains

4. If evidence is weak:
"Insufficient evidence from retrieved theses."

5. Use citations [1], [2], [3]

6. Do not create fake citations

==================================================
TASKS
==================================================

1. Summarize the retrieved research
2. Identify common research themes
3. Identify technologies used
4. Identify methodologies used
5. Identify weaknesses
6. Identify research gaps
7. Identify novelty opportunities
8. Suggest future research directions
9. Generate 10 thesis titles
10. Give a final recommendation

==================================================
OUTPUT FORMAT
==================================================

# Executive Summary

# Common Research Themes

# Technologies Used

# Methodologies Used

# Weaknesses of Existing Studies

# Research Gaps

# Novelty Opportunities

# Future Research Directions

# Recommended Thesis Titles

# Final Recommendation
"""


# =====================================
# RESEARCH ANALYSIS
# =====================================

def research_analysis(
    query: str,
    top_k: int = 10,
    mode: str = "analysis"
):

    # =================================
    # HYBRID SEARCH
    # =================================

    hybrid_results = hybrid_search(
        query=query,
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

    # =================================
    # NORMALIZE
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
        })

    theses = theses[:top_k]

    # =================================
    # DEBUG
    # =================================

    print("\n====================")
    print("RETRIEVED THESES")
    print("====================")

    for i, thesis in enumerate(
        theses,
        start=1
    ):

        print(f"\nTHESIS {i}")

        print(
            thesis.get(
                "title",
                "-"
            )
        )

        print(
            f"Score: {thesis.get('score', 0):.4f}"
        )

    # =================================
    # CITATION CONTEXT
    # =================================

    citation_results = []

    for thesis in theses:

        citation_results.append({

            "payload": thesis,

            "score":
            thesis.get(
                "score",
                0
            )
        })

    context = build_citation_context(
        citation_results
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

            "source_id": idx,

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
            )
        })

    # =================================
    # PROMPT
    # =================================

    prompt = build_prompt_by_mode(

        mode=mode,

        query=query,

        context=context
    )

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

        "query": query,

        "mode": mode,

        "related_theses": theses,

        "citations": citations,

        "analysis": analysis
    }