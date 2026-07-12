from app.services.research.extraction_utils import (
    extract_canonical_technologies
)


def extract_technologies(
    text: str
):

    technologies = []

    for technology, _ in extract_canonical_technologies(
        text
    ):

        technologies.append(
            technology
        )

    return sorted(
        list(
            set(
                technologies
            )
        )
    )


def update_technology_counter(
    counter,
    text: str
):

    for technology in extract_technologies(
        text
    ):

        counter[
            technology
        ] += 1

