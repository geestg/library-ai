import re

from collections import Counter


# =====================================
# NORMALIZE TEXT
# =====================================

def normalize_text(
    text: str
):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================
# TITLE KEYWORDS
# =====================================

def extract_keywords_from_title(
    title: str
):

    if not title:

        return []

    stopwords = {

        "dan",
        "dengan",
        "untuk",
        "yang",
        "dalam",
        "berbasis",
        "studi",
        "kasus",
        "implementasi",
        "rancang",
        "bangun",
        "sistem",
        "informasi",
        "analisis",
        "pengembangan",
        "penerapan",
        "pada"
    }

    words = title.lower().split()

    return [

        word.strip(".,:;()[]{}!?")

        for word in words

        if len(word.strip(".,:;()[]{}!?")) > 3

        and word.strip(".,:;()[]{}!?") not in stopwords
    ]


# =====================================
# FORMAT COUNTER
# =====================================

def counter_to_structured_list(
    counter: Counter
):

    return [

        {
            "name": name,
            "count": count
        }

        for name, count

        in counter.most_common()
    ]


# =====================================
# EXTRACT EVIDENCE
# =====================================

def extract_evidence(
    theses: list
):

    technology_counter = Counter()

    methodology_counter = Counter()

    domain_counter = Counter()

    dataset_counter = Counter()

    metric_counter = Counter()

    keyword_counter = Counter()

    year_counter = Counter()

    for thesis in theses:

        # =============================
        # TECHNOLOGY
        # =============================

        for technology in thesis.get(
            "technologies",
            []
        ):

            technology_counter[
                technology
            ] += 1

        # =============================
        # METHODOLOGY
        # =============================

        for methodology in thesis.get(
            "methodologies",
            []
        ):

            methodology_counter[
                methodology
            ] += 1

        # =============================
        # DOMAIN
        # =============================

        for domain in thesis.get(
            "domains",
            []
        ):

            domain_counter[
                domain
            ] += 1

        # =============================
        # DATASET
        # =============================

        for dataset in thesis.get(
            "datasets",
            []
        ):

            dataset_counter[
                dataset
            ] += 1

        # =============================
        # METRIC
        # =============================

        for metric in thesis.get(
            "evaluation_metrics",
            []
        ):

            metric_counter[
                metric
            ] += 1

        # =============================
        # YEAR
        # =============================

        year = thesis.get(
            "year"
        )

        if year:

            year_counter[
                str(year)
            ] += 1

        # =============================
        # KEYWORDS
        # =============================

        title = thesis.get(
            "title",
            ""
        )

        for keyword in extract_keywords_from_title(
            title
        ):

            keyword_counter[
                keyword
            ] += 1

    print("\n")
    print("=" * 80)
    print("COUNTER DEBUG V4")
    print("=" * 80)

    print(
        "TECH:",
        technology_counter
    )

    print(
        "METHOD:",
        methodology_counter
    )

    print(
        "DOMAIN:",
        domain_counter
    )

    print(
        "DATASET:",
        dataset_counter
    )

    print(
        "METRIC:",
        metric_counter
    )

    print(
        "YEAR:",
        year_counter
    )

    print(
        "KEYWORD:",
        keyword_counter
    )

    return {

        "technologies":
        counter_to_structured_list(
            technology_counter
        ),

        "methodologies":
        counter_to_structured_list(
            methodology_counter
        ),

        "keywords":
        counter_to_structured_list(
            keyword_counter
        ),

        "research_domains":
        counter_to_structured_list(
            domain_counter
        ),

        "datasets":
        counter_to_structured_list(
            dataset_counter
        ),

        "evaluation_metrics":
        counter_to_structured_list(
            metric_counter
        ),

        "years":
        counter_to_structured_list(
            year_counter
        )
    }