TREND_KEYWORDS = [

    "tren",

    "trend",

    "top teknologi",

    "top metode",

    "top method",

    "top dataset",

    "research trend",

    "tren penelitian",

    "teknologi populer",

    "metode populer",

    "dataset populer",

    "emerging topic",

    "topik populer",

    "perkembangan penelitian"
]


def is_trend_query(
    query: str
):

    q = query.lower()

    return any(

        keyword in q

        for keyword in TREND_KEYWORDS

    )