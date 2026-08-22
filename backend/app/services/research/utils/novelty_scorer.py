# =====================================
# NOVELTY SCORER V2
# =====================================
def calculate_novelty_score(
    evidence_matrix,
    gap_analysis: dict
):

    if hasattr(evidence_matrix, "to_dict"):
        evidence_matrix = evidence_matrix.to_dict()
    elif not isinstance(evidence_matrix, dict):
        evidence_matrix = {}

    score = 0
    reasons = []

    # =================================
    # TECHNOLOGY RARITY
    # =================================
    technology_frequency = (
        evidence_matrix.get(
            "technology_frequency",
            {}
        )
    )

    rare_technologies = [
        technology
        for technology, count
        in technology_frequency.items()
        if count == 1
    ]

    technology_score = min(
        len(rare_technologies) * 8,
        25
    )

    if rare_technologies:
        reasons.append(
            f"Terdapat {len(rare_technologies)} teknologi yang masih jarang digunakan."
        )
    score += technology_score

    # =================================
    # DATASET RARITY
    # =================================
    dataset_frequency = (
        evidence_matrix.get(
            "dataset_frequency",
            {}
        )
    )

    rare_datasets = [
        dataset
        for dataset, count
        in dataset_frequency.items()
        if count == 1
    ]

    dataset_score = min(
        len(rare_datasets) * 7,
        20
    )

    if rare_datasets:
        reasons.append(
            f"Terdapat {len(rare_datasets)} dataset yang masih jarang digunakan."
        )
    score += dataset_score

    # =================================
    # TEMPORAL NOVELTY
    # =================================
    temporal_score = 0
    year_frequency = (
        evidence_matrix.get(
            "year_frequency",
            {}
        )
    )

    years = []

    for year in year_frequency.keys():
        try:
            years.append(
                int(year)
            )
        except Exception:
            pass

    if years:
        latest_year = max(
            years
        )
        latest_count = year_frequency.get(
            str(latest_year),
            0
        )
        if latest_count <= 1:
            temporal_score = 15
            reasons.append(
                f"Penelitian pada tahun {latest_year} masih relatif terbatas."
            )
        elif latest_count <= 2:
            temporal_score = 8
    score += temporal_score

    # =================================
    # GAP CONTRIBUTION
    # =================================
    gap_score = 0
    gap_score += min(
        len(
            gap_analysis.get(
                "method_gap",
                []
            )
        ) * 3,
        10
    )

    gap_score += min(
        len(
            gap_analysis.get(
                "dataset_gap",
                []
            )
        ) * 3,
        10
    )

    gap_score += min(
        len(
            gap_analysis.get(
                "evaluation_gap",
                []
            )
        ) * 2,
        5
    )

    gap_score += min(
        len(
            gap_analysis.get(
                "temporal_gap",
                []
            )
        ) * 2,
        5
    )

    if gap_score > 0:
        reasons.append(
            "Masih terdapat research gap yang dapat dieksplorasi."
        )
    score += gap_score

    # =================================
    # DOMAIN DENSITY
    # =================================
    domain_frequency = (
        evidence_matrix.get(
            "domain_frequency",
            {}
        )
    )

    domain_score = 0

    if len(domain_frequency) <= 2:
        domain_score = 10

        reasons.append(
            "Domain penelitian masih relatif sempit sehingga peluang eksplorasi masih terbuka."
        )

    elif len(domain_frequency) <= 4:
        domain_score = 5
    score += domain_score

    # =================================
    # NORMALIZATION
    # =================================
    novelty_score = min(
        score,
        100
    )

    # =================================
    # LEVEL
    # =================================
    if novelty_score >= 75:
        novelty_level = "HIGH"
    elif novelty_score >= 45:
        novelty_level = "MEDIUM"

    else:
        novelty_level = "LOW"

    # =================================
    # RETURN
    # =================================
    return {
        "novelty_score":
        novelty_score,

        "novelty_level":
        novelty_level,

        "technology_score":
        technology_score,

        "dataset_score":
        dataset_score,

        "temporal_score":
        temporal_score,

        "gap_score":
        gap_score,

        "domain_score":
        domain_score,

        "reasons":
        reasons
    }