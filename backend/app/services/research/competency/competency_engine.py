from collections import Counter

from app.services.research.competency.competency_mapping import (
    COMPETENCY_MAPPING
)


def build_competencies(
    evidence: dict
):

    counter = Counter()

    technologies = evidence.get(
        "technologies",
        []
    )

    for item in technologies:

        technology = item["name"]

        competencies = (

            COMPETENCY_MAPPING.get(
                technology,
                []
            )
        )

        for competency in competencies:

            counter[
                competency
            ] += item["count"]

    return [

        {
            "name": name,
            "count": count
        }

        for name, count

        in counter.most_common()
    ]

