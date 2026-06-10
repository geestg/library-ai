import re

from app.services.research.evidence_extractor import (
    HIGH_CONFIDENCE_TECHNOLOGIES,
    LOW_CONFIDENCE_TECHNOLOGIES,
    HIGH_CONFIDENCE_METHODOLOGIES,
    LOW_CONFIDENCE_METHODOLOGIES,
    DATASET_PATTERNS,
    METRIC_PATTERNS,
    normalize_text,
    contains_term
)


def extract_thesis_evidence(
    thesis: dict
):

    title = thesis.get(
        "title",
        ""
    )

    abstract = thesis.get(
        "abstract",
        ""
    )

    chunk = thesis.get(
        "chunk",
        ""
    )

    text = normalize_text(
        f"{title}\n{abstract}\n{chunk}"
    )

    technologies = []
    methodologies = []
    datasets = []
    metrics = []

    # ==========================
    # TECHNOLOGIES
    # ==========================

    for tech in HIGH_CONFIDENCE_TECHNOLOGIES:

        if contains_term(
            text,
            tech
        ):

            technologies.append(
                tech
            )

    for tech in LOW_CONFIDENCE_TECHNOLOGIES:

        occurrences = len(

            re.findall(

                rf"\b{re.escape(tech)}\b",

                text,

                flags=re.IGNORECASE
            )
        )

        if occurrences >= 2:

            technologies.append(
                tech
            )

    # ==========================
    # METHODOLOGIES
    # ==========================

    for method in HIGH_CONFIDENCE_METHODOLOGIES:

        if contains_term(
            text,
            method
        ):

            methodologies.append(
                method
            )

    for method in LOW_CONFIDENCE_METHODOLOGIES:

        occurrences = len(

            re.findall(

                rf"\b{re.escape(method)}\b",

                text,

                flags=re.IGNORECASE
            )
        )

        if occurrences >= 2:

            methodologies.append(
                method
            )

    # ==========================
    # DATASETS
    # ==========================

    for dataset in DATASET_PATTERNS:

        if contains_term(
            text,
            dataset
        ):

            datasets.append(
                dataset
            )

    # ==========================
    # METRICS
    # ==========================

    for metric in METRIC_PATTERNS:

        if contains_term(
            text,
            metric
        ):

            metrics.append(
                metric
            )

    return {

        "technologies":
        technologies,

        "methodologies":
        methodologies,

        "datasets":
        datasets,

        "evaluation_metrics":
        metrics
    }