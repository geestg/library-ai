from .response_modes import (
    RESPONSE_MODES,
)


def detect_response_mode(
    query: str,
) -> tuple[str, str]:

    query = query.lower()

    if any(word in query for word in (

        "research gap",
        "gap penelitian",
        "novelty",
        "future work",

    )):

        mode = "research_gap"

    elif any(word in query for word in (

        "metodologi",
        "metode",
        "algoritma",
        "framework",

    )):

        mode = "methodology"

    elif any(word in query for word in (

        "literature review",
        "state of the art",
        "related work",
        "penelitian sebelumnya",

    )):

        mode = "literature"

    elif any(word in query for word in (

        "arsitektur",
        "transformer",
        "cnn",
        "svm",
        "embedding",
        "fine tuning",

    )):

        mode = "technical"

    else:

        mode = "academic"

    return (
        mode,
        RESPONSE_MODES[mode],
    )
