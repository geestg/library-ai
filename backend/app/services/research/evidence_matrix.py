from app.services.research.models.evidence_analysis import (
    EvidenceAnalysis
)

from app.services.research.models.evidence_matrix import (
    EvidenceMatrix
)


# =====================================
# BUILD EVIDENCE MATRIX V3
# =====================================

def build_evidence_matrix(
    evidence
):

    if isinstance(
        evidence,
        dict
    ):

        evidence = (
            EvidenceAnalysis.from_dict(
                evidence
            )
        )

    matrix = EvidenceMatrix()

    # =================================
    # TECHNOLOGY
    # =================================

    for item in evidence.technologies:

        matrix.technology_frequency[
            item.name
        ] = item.count

    # =================================
    # METHODOLOGY
    # =================================

    for item in evidence.methodologies:

        matrix.methodology_frequency[
            item.name
        ] = item.count

    # =================================
    # KEYWORD
    # =================================

    for item in evidence.keywords:

        matrix.keyword_frequency[
            item.name
        ] = item.count

    # =================================
    # DOMAIN
    # =================================

    for item in evidence.research_domains:

        matrix.domain_frequency[
            item.name
        ] = item.count

    # =================================
    # DATASET
    # =================================

    for item in evidence.datasets:

        matrix.dataset_frequency[
            item.name
        ] = item.count

    # =================================
    # METRIC
    # =================================

    for item in evidence.evaluation_metrics:

        matrix.evaluation_frequency[
            item.name
        ] = item.count

    # =================================
    # YEAR
    # =================================

    for item in evidence.years:

        matrix.year_frequency[
            item.name
        ] = item.count

    # =================================
    # DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("EVIDENCE MATRIX V3")
    print("=" * 80)

    print(
        "TECHNOLOGY:",
        matrix.technology_frequency
    )

    print(
        "METHODOLOGY:",
        matrix.methodology_frequency
    )

    print(
        "DOMAIN:",
        matrix.domain_frequency
    )

    print(
        "DATASET:",
        matrix.dataset_frequency
    )

    print(
        "METRIC:",
        matrix.evaluation_frequency
    )

    print(
        "YEAR:",
        matrix.year_frequency
    )

    return matrix
