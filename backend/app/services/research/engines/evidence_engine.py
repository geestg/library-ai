from app.services.research.evidence_extractor import (
    extract_evidence
)

from app.services.research.evidence_matrix import (
    build_evidence_matrix
)

from app.services.research.gap_detector import (
    detect_research_gaps
)

from app.services.research.novelty_scorer import (
    calculate_novelty_score
)

from app.services.research.trend_engine import (
    build_research_trends
)

from app.services.research.models.research_context import (
    ResearchContext
)

from app.services.research.competency.competency_engine import (
    build_competencies
)

# =====================================
# EVIDENCE PIPELINE
# =====================================

def run_evidence_pipeline(
    context: ResearchContext
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
    # TREND ANALYSIS
    # =================================

    context.trend_analysis = (
        build_research_trends(
            context.evidence_matrix
        )
    )

    # =================================
    # GAP ANALYSIS
    # =================================

    context.gap_analysis = (
        detect_research_gaps(
            context.evidence_matrix
        )
    )

    # =================================
    # NOVELTY ANALYSIS
    # =================================

    context.novelty_analysis = (
        calculate_novelty_score(

            context.evidence_matrix,

            context.gap_analysis
        )
    )

    context.competency_analysis = {

        "competencies":

        build_competencies(
            context.evidence
        )
    }

    return context