from app.services.research.gap.common import (
    get_dominant_items,
    unique_keep_order
)


# =====================================
# DOMINANT TOPIC DETECTOR
# =====================================

def detect_dominant_topics(

    technology_frequency,

    methodology_frequency,

    domain_frequency
):

    dominant_topics = []

    frequency_groups = [

        technology_frequency,

        methodology_frequency,

        domain_frequency
    ]

    for frequency in frequency_groups:

        dominant_topics.extend(

            get_dominant_items(
                frequency
            )
        )

    return unique_keep_order(
        dominant_topics
    )