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

    profile = context.research_profile

    evidence_text = build_evidence_section(
        context.evidence
    )

    matrix_text = build_matrix_section(
        context.evidence_matrix
    )

    trend_text = str(
        profile.trend.to_dict()
    )

    gap_text = str(
        profile.gap.to_dict()
    )

    novelty_text = str(
        profile.novelty.to_dict()
    )

    competency_text = str(
        profile.competency.to_dict()
    )

    prodi_text = str(
        profile.prodi.to_dict()
    )

    return (

        evidence_text

        + "\n\n"

        + matrix_text

        + "\n\n"

        + "TREND ANALYSIS\n"

        + "=" * 50

        + "\n"

        + trend_text

        + "\n\n"

        + "GAP ANALYSIS\n"

        + "=" * 50

        + "\n"

        + gap_text

        + "\n\n"

        + "NOVELTY ANALYSIS\n"

        + "=" * 50

        + "\n"

        + novelty_text

        + "\n\n"

        + "COMPETENCY ANALYSIS\n"

        + "=" * 50

        + "\n"

        + competency_text

        + "\n\n"

        + "PROGRAM STUDY ANALYSIS\n"

        + "=" * 50

        + "\n"

        + prodi_text
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