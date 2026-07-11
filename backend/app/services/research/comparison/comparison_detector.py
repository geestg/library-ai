COMPARE_KEYWORDS = [

    "bandingkan",

    "perbandingan",

    "compare",

    "versus",

    "vs",

    "lebih baik"
]


def normalize_text(
    text: str
):

    if not text:
        return ""

    return text.lower().strip()


def is_comparison_query(
    query: str
):

    query = normalize_text(
        query
    )

    return any(

        keyword in query

        for keyword

        in COMPARE_KEYWORDS
    )
