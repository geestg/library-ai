# =====================================
# RESEARCH TREND ENGINE V1
# =====================================

def build_research_trends(
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

    dataset_frequency = (
        evidence_matrix.get(
            "dataset_frequency",
            {}
        )
    )

    # =================================
    # TOP TECHNOLOGIES
    # =================================

    top_technologies = sorted(

        technology_frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )[:5]

    # =================================
    # TOP METHODS
    # =================================

    top_methods = sorted(

        methodology_frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )[:5]

    # =================================
    # TOP DATASETS
    # =================================

    top_datasets = sorted(

        dataset_frequency.items(),

        key=lambda x: x[1],

        reverse=True

    )[:5]

    # =================================
    # EMERGING TOPICS
    # =================================

    emerging_topics = [

        name

        for name, count

        in technology_frequency.items()

        if count == 2

    ]

    # =================================
    # TREND NARRATIVE
    # =================================

    trend_summary = []

    if top_technologies:

        trend_summary.append(

            f"Teknologi yang paling sering muncul adalah {top_technologies[0][0]}."

        )

    if top_methods:

        trend_summary.append(

            f"Metodologi yang paling dominan adalah {top_methods[0][0]}."

        )

    if top_datasets:

        trend_summary.append(

            f"Dataset yang paling sering digunakan adalah {top_datasets[0][0]}."

        )

    return {

        "top_technologies":
        top_technologies,

        "top_methods":
        top_methods,

        "top_datasets":
        top_datasets,

        "emerging_topics":
        emerging_topics,

        "research_trends":
        trend_summary
    }