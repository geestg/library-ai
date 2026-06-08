# =====================================
# NOVELTY SCORER V1
# =====================================

def calculate_novelty_score(

    evidence_matrix: dict,

    gap_analysis: dict
):

    score = 0

    reasons = []

    # =================================
    # METHOD GAP
    # =================================

    method_gap = gap_analysis.get(
        "method_gap",
        []
    )

    if method_gap:

        score += 2

        reasons.append(
            "Terdapat peluang penggunaan metodologi yang masih jarang digunakan."
        )

    # =================================
    # DATASET GAP
    # =================================

    dataset_gap = gap_analysis.get(
        "dataset_gap",
        []
    )

    if dataset_gap:

        score += 2

        reasons.append(
            "Masih terdapat dataset yang belum banyak dieksplorasi."
        )

    # =================================
    # TEMPORAL GAP
    # =================================

    temporal_gap = gap_analysis.get(
        "temporal_gap",
        []
    )

    if temporal_gap:

        score += 2

        reasons.append(
            "Penelitian terbaru pada topik ini masih terbatas."
        )

    # =================================
    # EVALUATION GAP
    # =================================

    evaluation_gap = gap_analysis.get(
        "evaluation_gap",
        []
    )

    if evaluation_gap:

        score += 2

        reasons.append(
            "Evaluasi penelitian sebelumnya masih belum komprehensif."
        )

    # =================================
    # DOMAIN DENSITY
    # =================================

    domain_frequency = (

        evidence_matrix.get(
            "domain_frequency",
            {}
        )
    )

    if len(domain_frequency) <= 2:

        score += 1

        reasons.append(
            "Domain penelitian masih relatif sempit."
        )

    # =================================
    # TECHNOLOGY DENSITY
    # =================================

    technology_frequency = (

        evidence_matrix.get(
            "technology_frequency",
            {}
        )
    )

    dominant_count = len([

        item

        for item in technology_frequency.values()

        if item >= 3

    ])

    if dominant_count <= 1:

        score += 1

        reasons.append(
            "Belum terdapat dominasi teknologi yang kuat."
        )

    # =================================
    # NORMALIZATION
    # =================================

    novelty_score = min(

        round(
            score,
            1
        ),

        10
    )

    # =================================
    # LABEL
    # =================================

    if novelty_score >= 8:

        novelty_level = "HIGH"

    elif novelty_score >= 5:

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

        "reasons":
        reasons
    }