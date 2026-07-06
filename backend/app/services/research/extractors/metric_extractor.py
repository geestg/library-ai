from app.services.research.extraction_utils import (
    extract_canonical_metrics
)


def extract_metrics(
    text: str
):

    metrics = []

    for metric, _ in extract_canonical_metrics(
        text
    ):

        metrics.append(
            metric
        )

    return sorted(
        list(
            set(
                metrics
            )
        )
    )


def update_metric_counter(
    counter,
    text: str
):

    for metric in extract_metrics(
        text
    ):

        counter[
            metric
        ] += 1