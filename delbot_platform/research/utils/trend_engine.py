from delbot_platform.research.models.research_models import (
    EvidenceMatrix
)

# =====================================
# RESEARCH TREND ENGINE V2
# =====================================
def build_research_trends(
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

    # =================================
    # TOP ITEMS
    # =================================
    top_technologies = (
        evidence_matrix.top_technologies()
    )
    top_methods = (
        evidence_matrix.top_methodologies()
    )
    top_datasets = (
        evidence_matrix.top_datasets()
    )

    # =================================
    # EMERGING TECHNOLOGIES
    # =================================
    emerging_topics = [
        name
        for name, count
        in evidence_matrix
        .technology_frequency
        .items()
        if count == 2
    ]

    # =================================
    # TREND SUMMARY
    # =================================
    trend_summary = []
    if top_technologies:
        trend_summary.append(
            f"Teknologi yang paling dominan adalah "
            f"{top_technologies[0][0]} "
            f"dengan frekuensi "
            f"{top_technologies[0][1]}."
        )

    if top_methods:
        trend_summary.append(
            f"Metodologi yang paling dominan adalah "
            f"{top_methods[0][0]}."
        )

    if top_datasets:
        trend_summary.append(
            f"Dataset yang paling sering digunakan adalah "
            f"{top_datasets[0][0]}."
        )

    latest_year = (
        evidence_matrix.latest_year()
    )

    if latest_year:
        trend_summary.append(
            f"Penelitian terbaru berasal dari tahun "
            f"{latest_year}."
        )

    # =================================
    # RETURN
    # =================================

    return {

        "top_technologies":
        top_technologies,

        "top_methods":
        top_methods,

        "top_datasets":
        top_datasets,

        "emerging_topics":
        emerging_topics,

        "latest_year":
        latest_year,

        "research_trends":
        trend_summary
    }