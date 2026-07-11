from app.services.research.comparison.method_extractor import (
    extract_methods
)

from app.services.research.comparison.comparison_matrix_builder import (
    build_comparison_matrix
)

from app.services.research.comparison.comparison_prompt_builder import (
    build_comparison_prompt
)

from app.services.research.comparison.comparison_llm import (
    generate_comparison_analysis
)


def run_method_comparison(
    query: str,
    theses: list
):

    methods = extract_methods(
        query
    )

    if len(methods) < 2:

        return {

            "mode":
            "comparison",

            "comparison":
            "Minimal dua metode diperlukan.",

            "comparison_matrix":
            {},

            "methods":
            methods
        }

    matrix = build_comparison_matrix(

        methods,

        theses
    )

    prompt = build_comparison_prompt(

        query=query,

        matrix=matrix
    )

    analysis = (
        generate_comparison_analysis(
            prompt
        )
    )

    return {

        "mode":
        "comparison",

        "methods":
        methods,

        "comparison_matrix":
        matrix,

        "comparison":
        analysis
    }
