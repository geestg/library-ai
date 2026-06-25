from app.services.research.prompt_builder import (
    build_evidence_section,
    build_matrix_section
)

# =====================================
# BUILD EVIDENCE CONTEXT
# =====================================

def build_evidence_context(

    evidence: dict,

    evidence_matrix: dict,

    gap_analysis: dict
):

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

    return {

        "evidence_text":
        evidence_text,

        "matrix_text":
        matrix_text,

        "combined_evidence":
        combined_evidence
    }