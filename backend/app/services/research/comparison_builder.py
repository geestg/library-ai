from collections import Counter


# =====================================
# SAFE TOP ITEMS
# =====================================

def top_items(
    frequency_dict,
    limit=5
):

    if not frequency_dict:
        return []

    return [

        {
            "name": name,
            "count": count
        }

        for name, count in sorted(

            frequency_dict.items(),

            key=lambda x: x[1],

            reverse=True

        )[:limit]
    ]


# =====================================
# METHOD PROFILE
# =====================================

def build_method_profile(

    method_name: str,

    theses: list,

    evidence: dict,

    evidence_matrix: dict
):

    return {

        "method":

        method_name,

        "frequency":

        evidence_matrix.get(
            "technology_frequency",
            {}
        ).get(
            method_name,
            0
        ),

        "domains":

        top_items(

            evidence_matrix.get(
                "domain_frequency",
                {}
            )
        ),

        "datasets":

        evidence.get(
            "datasets",
            []
        )[:5],

        "evaluation_metrics":

        evidence.get(
            "evaluation_metrics",
            []
        )[:5],

        "years":

        evidence.get(
            "years",
            []
        )[:5]
    }


# =====================================
# BUILD COMPARISON MATRIX
# =====================================

def build_comparison_matrix(

    methods: list,

    theses: list,

    evidence: dict,

    evidence_matrix: dict
):

    matrix = {}

    for method in methods:

        matrix[
            method
        ] = build_method_profile(

            method_name=method,

            theses=theses,

            evidence=evidence,

            evidence_matrix=evidence_matrix
        )

    return matrix

