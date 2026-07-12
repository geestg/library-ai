from app.services.research.models.evidence_matrix import (
    EvidenceMatrix
)


# =====================================
# NORMALIZE FREQUENCY INPUT
# =====================================

def normalize_frequency(
    frequency
):

    if frequency is None:

        return {}

    if isinstance(
        frequency,
        dict
    ):

        return frequency

    return dict(frequency)


# =====================================
# REMOVE DUPLICATE
# =====================================

def unique_keep_order(
    items
):

    seen = set()

    results = []

    for item in items:

        if item in seen:

            continue

        seen.add(item)

        results.append(item)

    return results


# =====================================
# DOMINANT ITEMS
# =====================================

def get_dominant_items(

    frequency,

    threshold: int = 3
):

    frequency = normalize_frequency(
        frequency
    )

    return [

        name

        for name, count

        in frequency.items()

        if count >= threshold
    ]


# =====================================
# EMERGING ITEMS
# =====================================

def get_emerging_items(
    frequency
):

    frequency = normalize_frequency(
        frequency
    )

    return [

        name

        for name, count

        in frequency.items()

        if count == 2
    ]


# =====================================
# RARE ITEMS
# =====================================

def get_rare_items(
    frequency
):

    frequency = normalize_frequency(
        frequency
    )

    return [

        name

        for name, count

        in frequency.items()

        if count == 1
    ]


# =====================================
# TOP ITEM
# =====================================

def get_top_item(
    frequency
):

    frequency = normalize_frequency(
        frequency
    )

    if not frequency:

        return None

    return max(

        frequency.items(),

        key=lambda item: item[1]
    )


# =====================================
# SORTED ITEMS
# =====================================

def get_sorted_items(
    frequency
):

    frequency = normalize_frequency(
        frequency
    )

    return sorted(

        frequency.items(),

        key=lambda item: item[1],

        reverse=True
    )


# =====================================
# TOTAL OCCURRENCES
# =====================================

def get_total_occurrences(
    frequency
):

    frequency = normalize_frequency(
        frequency
    )

    return sum(
        frequency.values()
    )

