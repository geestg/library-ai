from collections import Counter


# =====================================
# GAP DETECTOR V1
# =====================================

def detect_research_gaps(
    evidence_matrix: dict
):

    technology_frequency = (
        evidence_matrix.get(
            "technology_frequency",
            {}
        )
    )

    methodology_frequency = (
        evidence_matrix.get(
            "methodology_frequency",
            {}
        )
    )

    domain_frequency = (
        evidence_matrix.get(
            "domain_frequency",
            {}
        )
    )

    dominant_topics = []

    emerging_topics = []

    rare_topics = []

    # =================================
    # TECHNOLOGY ANALYSIS
    # =================================

    for name, count in (
        technology_frequency.items()
    ):

        if count >= 3:

            dominant_topics.append(
                name
            )

        elif count == 2:

            emerging_topics.append(
                name
            )

        else:

            rare_topics.append(
                name
            )

    # =================================
    # DOMAIN ANALYSIS
    # =================================

    for name, count in (
        domain_frequency.items()
    ):

        if count >= 3:

            if name not in dominant_topics:

                dominant_topics.append(
                    name
                )

        elif count == 2:

            if name not in emerging_topics:

                emerging_topics.append(
                    name
                )

    # =================================
    # MISSING EVIDENCE
    # =================================

    missing_evidence = []

    expected_dimensions = [

        "usability",
        "scalability",
        "security",
        "performance",
        "evaluation",
        "integration"
    ]

    all_terms = set()

    all_terms.update(
        technology_frequency.keys()
    )

    all_terms.update(
        methodology_frequency.keys()
    )

    all_terms.update(
        domain_frequency.keys()
    )

    for item in expected_dimensions:

        if item not in all_terms:

            missing_evidence.append(
                item
            )

    # =================================
    # GAP SCORE
    # =================================

    gap_score = len(
        missing_evidence
    )

    # =================================
    # RETURN
    # =================================

    return {

        "dominant_topics":
        dominant_topics,

        "emerging_topics":
        emerging_topics,

        "rare_topics":
        rare_topics,

        "missing_evidence":
        missing_evidence,

        "gap_score":
        gap_score
    }