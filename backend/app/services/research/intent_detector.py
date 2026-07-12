THESIS_IDEA_KEYWORDS = [

    "ide skripsi",
    "judul skripsi",
    "thesis idea",
    "research idea",
    "topik skripsi",
    "proposal skripsi",
    "novelty"
]

LITERATURE_REVIEW_KEYWORDS = [

    "literature review",
    "tinjauan pustaka",
    "state of the art",
    "penelitian terdahulu",
    "kajian pustaka",
    "bab 2"
]


def is_thesis_idea_query(
    query: str
):

    query = query.lower()

    return any(

        keyword in query

        for keyword

        in THESIS_IDEA_KEYWORDS
    )


def is_literature_review_query(
    query: str
):

    query = query.lower()

    return any(

        keyword in query

        for keyword

        in LITERATURE_REVIEW_KEYWORDS
    )

