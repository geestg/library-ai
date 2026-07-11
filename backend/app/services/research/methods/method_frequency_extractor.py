def extract_method_frequency(
    evidence_matrix: dict
):

    return evidence_matrix.get(
        "technology_frequency",
        {}
    )
