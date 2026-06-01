# =====================================
# BUILD EVIDENCE MATRIX
# =====================================

def build_evidence_matrix(
    evidence: dict
):

    matrix = {

        "technology_frequency": {},

        "methodology_frequency": {},

        "keyword_frequency": {},

        "domain_frequency": {}
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

    return matrix