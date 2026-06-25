import re


# =====================================
# COUNT ALIAS OCCURRENCES
# =====================================

def count_alias_occurrences(
    text: str,
    aliases: list
):

    total = 0

    for alias in aliases:

        total += len(

            re.findall(

                rf"\b{re.escape(alias)}\b",

                text,

                flags=re.IGNORECASE
            )
        )

    return total


# =====================================
# EXTRACT PATTERN ENTITIES
# =====================================

def extract_pattern_entities(
    text: str,
    patterns: dict
):

    results = []

    for canonical_name, aliases in patterns.items():

        occurrences = count_alias_occurrences(
            text,
            aliases
        )

        if occurrences > 0:

            results.append(

                (
                    canonical_name,
                    occurrences
                )
            )

    return results


# =====================================
# EXTRACT CANONICAL VALUES
# =====================================

def extract_canonical_values(
    text: str,
    patterns: dict
):

    values = []

    for canonical_name, aliases in patterns.items():

        for alias in aliases:

            if re.search(

                rf"\b{re.escape(alias)}\b",

                text,

                flags=re.IGNORECASE
            ):

                values.append(
                    canonical_name
                )

                break

    return values


# =====================================
# EXTRACT CANONICAL TECHNOLOGIES
# BACKWARD COMPATIBILITY
# =====================================

def extract_canonical_technologies(
    text: str
):

    from app.services.research.evidence_patterns import (
        TECHNOLOGY_PATTERNS
    )

    return extract_pattern_entities(
        text,
        TECHNOLOGY_PATTERNS
    )


# =====================================
# EXTRACT CANONICAL METHODOLOGIES
# =====================================

def extract_canonical_methodologies(
    text: str
):

    from app.services.research.evidence_patterns import (
        METHODOLOGY_PATTERNS
    )

    return extract_pattern_entities(
        text,
        METHODOLOGY_PATTERNS
    )


# =====================================
# EXTRACT CANONICAL DATASETS
# =====================================

def extract_canonical_datasets(
    text: str
):

    from app.services.research.evidence_patterns import (
        DATASET_PATTERNS
    )

    return extract_pattern_entities(
        text,
        DATASET_PATTERNS
    )


# =====================================
# EXTRACT CANONICAL METRICS
# =====================================

def extract_canonical_metrics(
    text: str
):

    from app.services.research.evidence_patterns import (
        METRIC_PATTERNS
    )

    return extract_pattern_entities(
        text,
        METRIC_PATTERNS
    )


# =====================================
# EXTRACT CANONICAL DOMAINS
# =====================================

def extract_canonical_domains(
    text: str
):

    from app.services.research.evidence_patterns import (
        DOMAIN_PATTERNS
    )

    return extract_pattern_entities(
        text,
        DOMAIN_PATTERNS
    )