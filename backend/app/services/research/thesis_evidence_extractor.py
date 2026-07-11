from app.services.research.evidence_extractor import (
    normalize_text
)

from app.services.research.extractors.technology_extractor import (
    extract_technologies
)

from app.services.research.extractors.methodology_extractor import (
    extract_methodologies
)

from app.services.research.extractors.domain_extractor import (
    extract_domains
)

from app.services.research.extractors.dataset_extractor import (
    extract_datasets
)

from app.services.research.extractors.metric_extractor import (
    extract_metrics
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

        f"""
        {title}
        {abstract}
        {chunk}
        """
    )

    return {

        "technologies":
        extract_technologies(
            text
        ),

        "methodologies":
        extract_methodologies(
            text
        ),

        "domains":
        extract_domains(
            text
        ),

        "datasets":
        extract_datasets(
            text
        ),

        "evaluation_metrics":
        extract_metrics(
            text
        )
    }
