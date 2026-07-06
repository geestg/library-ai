from app.services.research.gap.common import (
    get_rare_items,
    unique_keep_order
)


# =====================================
# RARE TOPIC DETECTOR
# =====================================

def detect_rare_topics(

    technology_frequency,

    methodology_frequency,

    domain_frequency
):

    rare_topics = []

    frequency_groups = [

        technology_frequency,

        methodology_frequency,

        domain_frequency
    ]

    for frequency in frequency_groups:

        rare_topics.extend(

            get_rare_items(
                frequency
            )
        )

    return unique_keep_order(
        rare_topics
    )