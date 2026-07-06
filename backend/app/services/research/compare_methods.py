from app.services.research.methods.method_frequency_extractor import (
    extract_method_frequency
)

from app.services.research.methods.method_comparison_builder import (
    build_method_entry
)

from app.services.research.methods.method_summary_builder import (
    build_method_summary
)


def compare_methods(
    evidence_matrix: dict
):

    method_frequency = (
        extract_method_frequency(
            evidence_matrix
        )
    )

    if not method_frequency:

        return {

            "summary":
            "Tidak ditemukan metode yang cukup untuk dibandingkan.",

            "methods":
            []
        }

    comparison = []

    sorted_methods = sorted(

        method_frequency.items(),

        key=lambda x: x[1],

        reverse=True
    )

    for method_name, frequency in sorted_methods:

        comparison.append(

            build_method_entry(

                method_name,

                frequency
            )
        )

    return {

        "summary":
        build_method_summary(
            sorted_methods
        ),

        "methods":
        comparison
    }