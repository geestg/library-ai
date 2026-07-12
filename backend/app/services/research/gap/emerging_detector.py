from app.services.research.gap.common import (
    get_emerging_items,
    unique_keep_order
)


# =====================================
# EMERGING TOPIC DETECTOR
# =====================================

def detect_emerging_topics(

    technology_frequency,

    methodology_frequency,

    domain_frequency
):

    emerging_topics = []

    frequency_groups = [

        technology_frequency,

        methodology_frequency,

        domain_frequency
    ]

    for frequency in frequency_groups:

        emerging_topics.extend(

            get_emerging_items(
                frequency
            )
        )

    return unique_keep_order(
        emerging_topics
    )

