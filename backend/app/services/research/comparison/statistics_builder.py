from collections import Counter


def build_method_statistics(
    method: str,
    theses: list
):

    matched = []

    domain_counter = Counter()

    dataset_counter = Counter()

    metric_counter = Counter()

    years = []

    for thesis in theses:

        thesis_technologies = [

            tech.lower()

            for tech in thesis.get(
                "technologies",
                []
            )
        ]

        thesis_methodologies = [

            methodology.lower()

            for methodology in thesis.get(
                "methodologies",
                []
            )
        ]

        is_match = (

            method.lower()
            in
            thesis_technologies

            or

            method.lower()
            in
            thesis_methodologies
        )

        if not is_match:
            continue

        matched.append(
            thesis
        )

        year = thesis.get(
            "year"
        )

        if year:

            years.append(
                str(year)
            )

        prodi = thesis.get(
            "prodi"
        )

        if prodi:

            domain_counter[
                prodi
            ] += 1

        for dataset in thesis.get(
            "datasets",
            []
        ):

            dataset_counter[
                dataset
            ] += 1

        for metric in thesis.get(
            "evaluation_metrics",
            []
        ):

            metric_counter[
                metric
            ] += 1

    return {

        "method":
        method,

        "frequency":
        len(matched),

        "years":
        sorted(
            list(
                set(years)
            )
        ),

        "domains":

        [

            item[0]

            for item

            in domain_counter.most_common(5)
        ],

        "datasets":

        [

            item[0]

            for item

            in dataset_counter.most_common(5)
        ],

        "evaluation_metrics":

        [

            item[0]

            for item

            in metric_counter.most_common(5)
        ]
    }