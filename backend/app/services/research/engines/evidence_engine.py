from app.services.research.evidence_extractor import (
    extract_evidence,
)

from app.services.research.evidence_matrix import (
    build_evidence_matrix,
)

from app.services.research.gap_detector import (
    detect_research_gaps,
)

from app.services.research.novelty_scorer import (
    calculate_novelty_score,
)

from app.services.research.trend_engine import (
    build_research_trends,
)

from app.services.research.models.research_context import (
    ResearchContext,
)

from app.services.research.models.trend_analysis import (
    TrendAnalysis,
)

from app.services.research.models.gap_analysis import (
    GapAnalysis,
)

from app.services.research.models.novelty_analysis import (
    NoveltyAnalysis,
)


# =====================================
# EVIDENCE PIPELINE
# =====================================

def run_evidence_pipeline(
    context: ResearchContext,
):

    print("\n====================================")
    print("EVIDENCE PIPELINE")
    print("====================================")

    # =================================
    # EVIDENCE EXTRACTION
    # =================================

    context.evidence = (
        extract_evidence(
            context.theses
        )
    )

    # =================================
    # EVIDENCE MATRIX
    # =================================

    context.evidence_matrix = (
        build_evidence_matrix(
            context.evidence
        )
    )

    # =================================
    # TREND
    # =================================

    context.research_profile.trend = (
        TrendAnalysis.from_dict(
            build_research_trends(
                context.evidence_matrix
            )
        )
    )

    # =================================
    # GAP
    # =================================

    context.research_profile.gap = (
        GapAnalysis.from_dict(
            detect_research_gaps(
                context.evidence_matrix
            )
        )
    )

    # =================================
    # NOVELTY
    # =================================

    context.research_profile.novelty = (
        NoveltyAnalysis.from_dict(
            calculate_novelty_score(

                context.evidence_matrix,

                context.research_profile.gap.to_dict(),

            )
        )
    )


    return context
