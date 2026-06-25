from app.rag.context_synthesizer import (
    build_citation_context
)

from app.services.research.prompt_builder import (
    build_evidence_section,
    build_matrix_section
)

from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# BUILD CITATION RESULTS
# =====================================

def build_citation_results(
    theses: list
):

    results = []

    for thesis in theses:

        results.append({

            "payload":
            thesis,

            "score":
            thesis.get(
                "score",
                0
            )
        })

    return results


# =====================================
# BUILD COMBINED EVIDENCE
# =====================================

def build_combined_evidence(
    context: ResearchContext
):

    evidence_text = (
        build_evidence_section(
            context.evidence
        )
    )

    matrix_text = (
        build_matrix_section(
            context.evidence_matrix
        )
    )

    return (

        evidence_text

        + "\n\n"

        + matrix_text

        + "\n\n"

        + "GAP ANALYSIS\n"

        + "=" * 50

        + "\n"

        + str(
            context.gap_analysis
        )
    )


# =====================================
# CONTEXT PIPELINE
# =====================================

def run_context_pipeline(
    context: ResearchContext
):

    context.combined_evidence = (
        build_combined_evidence(
            context
        )
    )

    citation_results = (
        build_citation_results(
            context.theses
        )
    )

    context.citation_context = (
        build_citation_context(
            citation_results
        )
    )

    return context