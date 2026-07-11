from app.services.research.extraction_utils import (
    extract_canonical_methodologies
)


def extract_methodologies(
    text: str
):

    methodologies = []

    for methodology, _ in extract_canonical_methodologies(
        text
    ):

        methodologies.append(
            methodology
        )

    return sorted(
        list(
            set(
                methodologies
            )
        )
    )


def update_methodology_counter(
    counter,
    text: str
):

    for methodology in extract_methodologies(
        text
    ):

        counter[
            methodology
        ] += 1
