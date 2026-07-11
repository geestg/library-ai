from app.services.research.comparison.statistics_builder import (
    build_method_statistics
)


def build_comparison_matrix(
    methods: list,
    theses: list
):

    matrix = {}

    for method in methods:

        matrix[
            method
        ] = build_method_statistics(
            method,
            theses
        )

    return matrix
