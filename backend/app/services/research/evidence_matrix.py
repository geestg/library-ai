# =====================================
# BUILD EVIDENCE MATRIX V2
# =====================================

def build_evidence_matrix(
    evidence: dict
):

    matrix = {

        "technology_frequency": {},

        "methodology_frequency": {},

        "keyword_frequency": {},

        "domain_frequency": {},

        "dataset_frequency": {},

        "metric_frequency": {},

        "year_frequency": {}
    }

    # =================================
    # TECHNOLOGY
    # =================================

    for item in evidence.get(
        "technologies",
        []
    ):

        matrix[
            "technology_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # METHODOLOGY
    # =================================

    for item in evidence.get(
        "methodologies",
        []
    ):

        matrix[
            "methodology_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # KEYWORD
    # =================================

    for item in evidence.get(
        "keywords",
        []
    ):

        matrix[
            "keyword_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # DOMAIN
    # =================================

    for item in evidence.get(
        "research_domains",
        []
    ):

        matrix[
            "domain_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # DATASET
    # =================================

    for item in evidence.get(
        "datasets",
        []
    ):

        matrix[
            "dataset_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # EVALUATION METRICS
    # =================================

    for item in evidence.get(
        "evaluation_metrics",
        []
    ):

        matrix[
            "metric_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # YEARS
    # =================================

    for item in evidence.get(
        "years",
        []
    ):

        matrix[
            "year_frequency"
        ][
            item["name"]
        ] = item["count"]

    # =================================
    # DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("EVIDENCE MATRIX V2")
    print("=" * 80)

    print(
        "TECHNOLOGY:",
        matrix["technology_frequency"]
    )

    print(
        "METHODOLOGY:",
        matrix["methodology_frequency"]
    )

    print(
        "DOMAIN:",
        matrix["domain_frequency"]
    )

    print(
        "DATASET:",
        matrix["dataset_frequency"]
    )

    print(
        "METRIC:",
        matrix["metric_frequency"]
    )

    print(
        "YEAR:",
        matrix["year_frequency"]
    )

    return matrix