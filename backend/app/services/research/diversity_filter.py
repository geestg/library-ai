from collections import defaultdict

# =====================================
# DIVERSITY FILTER
# =====================================

def apply_diversity_filter(

    theses: list,

    max_per_year: int = 2,

    max_per_title_keyword: int = 2
):

    filtered = []

    year_counter = defaultdict(int)

    keyword_counter = defaultdict(int)

    for thesis in theses:

        title = (
            thesis.get(
                "title",
                ""
            ) or ""
        ).lower()

        year = str(

            thesis.get(
                "year",
                "unknown"
            )

        )

        # =========================
        # MAIN KEYWORD
        # =========================

        keyword = "general"

        for candidate in [

            "cnn",
            "transformer",
            "bert",
            "lstm",
            "gru",
            "rag",
            "svm",
            "random forest",
            "yolo",
            "resnet",
            "mobilenet",
            "xgboost"
        ]:

            if candidate in title:

                keyword = candidate

                break

        # =========================
        # LIMIT YEAR
        # =========================

        if (

            year_counter[year]

            >=

            max_per_year

        ):

            continue

        # =========================
        # LIMIT TOPIC
        # =========================

        if (

            keyword_counter[keyword]

            >=

            max_per_title_keyword

        ):

            continue

        filtered.append(
            thesis
        )

        year_counter[
            year
        ] += 1

        keyword_counter[
            keyword
        ] += 1

    print("\n====================================")
    print("DIVERSITY FILTER")
    print("====================================")

    print(
        "YEAR COUNTS:",
        dict(year_counter)
    )

    print(
        "TOPIC COUNTS:",
        dict(keyword_counter)
    )

    print(
        f"FINAL: {len(filtered)}"
    )

    return filtered
