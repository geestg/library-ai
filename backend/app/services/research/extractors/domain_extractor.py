from app.services.research.extraction_utils import (
    extract_canonical_domains
)


def extract_domains(
    text: str
):

    domains = []

    for domain, _ in extract_canonical_domains(
        text
    ):

        domains.append(
            domain
        )

    return sorted(
        list(
            set(
                domains
            )
        )
    )


def update_domain_counter(
    counter,
    text: str
):

    for domain in extract_domains(
        text
    ):

        counter[
            domain
        ] += 1
