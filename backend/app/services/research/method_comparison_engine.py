from app.services.research.comparison.comparison_detector import (
    is_comparison_query
)

from app.services.research.comparison.method_extractor import (
    extract_methods
)

from app.services.research.comparison.statistics_builder import (
    build_method_statistics
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

from app.services.research.comparison.comparison_engine import (
    run_method_comparison
)

__all__ = [

    "is_comparison_query",

    "extract_methods",

    "build_method_statistics",

    "build_comparison_matrix",

    "build_comparison_prompt",

    "generate_comparison_analysis",

    "run_method_comparison"
]