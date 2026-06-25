from app.services.research.models.research_context import (
    ResearchContext
)

from app.services.research.engines.search_engine import (
    run_search_pipeline
)

from app.services.research.engines.domain_engine import (
    run_domain_pipeline
)

from app.services.research.engines.evidence_engine import (
    run_evidence_pipeline
)

from app.services.research.engines.context_engine import (
    run_context_pipeline
)

from app.services.research.engines.prompt_engine import (
    run_prompt_pipeline
)

from app.services.research.engines.llm_engine import (
    run_llm_pipeline
)

from app.services.research.engines.document_engine import (
    run_document_analysis
)

from app.services.research.engines.comparison_engine import (
    run_comparison_pipeline
)

from app.services.research.engines.literature_engine import (
    run_literature_review_pipeline
)

from app.services.research.engines.thesis_idea_engine import (
    run_thesis_idea_pipeline
)

from app.services.research.engines.response_engine import (
    build_research_response
)

from app.services.research.engines.prodi_engine import (
    run_prodi_pipeline
)

from app.services.research.engines.competency_engine import (
    run_competency_pipeline
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
    print("RESEARCH ENGINE V4")
    print("====================================")

    context = ResearchContext(

        query=query,

        top_k=top_k,

        mode=mode,

        active_document_ids=
        active_document_ids or []
    )

    # =================================
    # DOCUMENT MODE
    # =================================

    if context.active_document_ids:

        document_result = (
            run_document_analysis(

                query=context.query,

                active_document_ids=
                context.active_document_ids
            )
        )

        if document_result:

            return document_result

    # =================================
    # SEARCH
    # =================================

    run_search_pipeline(
        context
    )

    # =================================
    # DOMAIN
    # =================================

    run_domain_pipeline(
        context
    )

    # =================================
    # COMPARISON
    # =================================

    comparison_response = (
        run_comparison_pipeline(
            context
        )
    )

    if comparison_response:

        return comparison_response

    # =================================
    # DEBUG
    # =================================

    print("\n====================================")
    print("TOP THESIS")
    print("====================================")

    for idx, thesis in enumerate(
        context.theses,
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

    print("\n")
    print("=" * 80)
    print("THESIS DEBUG")
    print("=" * 80)

    for idx, thesis in enumerate(
        context.theses,
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
    # EVIDENCE
    # =================================

    run_evidence_pipeline(
        context
    )

    run_prodi_pipeline(
        context
    )

    # =================================
    # THESIS IDEA
    # =================================

    idea_response = (
        run_thesis_idea_pipeline(
            context
        )
    )
    if idea_response:

        return idea_response

    # =================================
    # CONTEXT
    # =================================

    run_context_pipeline(
        context
    )

    # =================================
    # LITERATURE REVIEW
    # =================================

    literature_response = (
        run_literature_review_pipeline(
            context
        )
    )

    if literature_response:

        return literature_response

    # =================================
    # PROMPT
    # =================================

    run_prompt_pipeline(
        context
    )

    # =================================
    # LLM
    # =================================

    run_llm_pipeline(
        context
    )

    # =================================
    # RESPONSE
    # =================================

    return build_research_response(
        context
    )