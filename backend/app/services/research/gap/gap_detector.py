from app.services.research.models.evidence_matrix import (
    EvidenceMatrix
)

from app.services.research.gap.dominant_detector import (
    detect_dominant_topics
)

from app.services.research.gap.emerging_detector import (
    detect_emerging_topics
)

from app.services.research.gap.rarity_detector import (
    detect_rare_topics
)

from app.services.research.gap.method_gap_detector import (
    detect_method_gap
)

from app.services.research.gap.dataset_gap_detector import (
    detect_dataset_gap
)

from app.services.research.gap.temporal_gap_detector import (
    detect_temporal_gap
)

from app.services.research.gap.evaluation_gap_detector import (
    detect_evaluation_gap
)

from app.services.research.gap.novelty_detector import (
    detect_novelty_opportunities
)

from app.services.research.gap.gap_scoring import (
    calculate_gap_score
)


# =====================================
# GAP DETECTOR V5
# =====================================

def detect_research_gaps(
    evidence_matrix
):

    if isinstance(
        evidence_matrix,
        dict
    ):

        evidence_matrix = (
            EvidenceMatrix.from_dict(
                evidence_matrix
            )
        )

    technology_frequency = (
        evidence_matrix.technology_frequency
    )

    methodology_frequency = (
        evidence_matrix.methodology_frequency
    )

    domain_frequency = (
        evidence_matrix.domain_frequency
    )

    dataset_frequency = (
        evidence_matrix.dataset_frequency
    )

    evaluation_frequency = (
        evidence_matrix.evaluation_frequency
    )

    year_frequency = (
        evidence_matrix.year_frequency
    )

    # =================================
    # DOMINANT
    # =================================

    dominant_topics = (
        detect_dominant_topics(

            technology_frequency,

            methodology_frequency,

            domain_frequency
        )
    )

    # =================================
    # EMERGING
    # =================================

    emerging_topics = (
        detect_emerging_topics(

            technology_frequency,

            methodology_frequency,

            domain_frequency
        )
    )

    # =================================
    # RARE
    # =================================

    rare_topics = (
        detect_rare_topics(

            technology_frequency,

            methodology_frequency,

            domain_frequency
        )
    )

    # =================================
    # METHOD GAP
    # =================================

    method_gap = (
        detect_method_gap(
            methodology_frequency
        )
    )

    # =================================
    # DATASET GAP
    # =================================

    dataset_gap = (
        detect_dataset_gap(
            dataset_frequency
        )
    )

    # =================================
    # TEMPORAL GAP
    # =================================

    temporal_gap = (
        detect_temporal_gap(
            year_frequency
        )
    )

    # =================================
    # EVALUATION GAP
    # =================================

    evaluation_gap = (
        detect_evaluation_gap(
            evaluation_frequency
        )
    )

    # =================================
    # NOVELTY OPPORTUNITY
    # =================================

    novelty_opportunities = (
        detect_novelty_opportunities(

            rare_topics,

            emerging_topics,

            dataset_frequency
        )
    )

    # =================================
    # GAP SCORE
    # =================================

    gap_score = (
        calculate_gap_score(

            method_gap,

            dataset_gap,

            temporal_gap,

            evaluation_gap
        )
    )

    # =================================
    # DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("GAP DETECTOR V5")
    print("=" * 80)

    print(
        "DOMINANT:",
        dominant_topics
    )

    print(
        "EMERGING:",
        emerging_topics
    )

    print(
        "RARE:",
        rare_topics
    )

    print(
        "METHOD GAP:",
        method_gap
    )

    print(
        "DATASET GAP:",
        dataset_gap
    )

    print(
        "TEMPORAL GAP:",
        temporal_gap
    )

    print(
        "EVALUATION GAP:",
        evaluation_gap
    )

    print(
        "NOVELTY:",
        novelty_opportunities
    )

    print(
        "GAP SCORE:",
        gap_score
    )

    return {

        "dominant_topics":
        dominant_topics,

        "emerging_topics":
        emerging_topics,

        "rare_topics":
        rare_topics,

        "method_gap":
        method_gap,

        "dataset_gap":
        dataset_gap,

        "temporal_gap":
        temporal_gap,

        "evaluation_gap":
        evaluation_gap,

        "novelty_opportunities":
        novelty_opportunities,

        "gap_score":
        gap_score
    }

