from app.services.research.extraction_utils import (
    extract_canonical_datasets
)


def extract_datasets(
    text: str
):

    datasets = []

    for dataset, _ in extract_canonical_datasets(
        text
    ):

        datasets.append(
            dataset
        )

    return sorted(
        list(
            set(
                datasets
            )
        )
    )


def update_dataset_counter(
    counter,
    text: str
):

    for dataset in extract_datasets(
        text
    ):

        counter[
            dataset
        ] += 1

