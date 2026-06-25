from app.services.research.gap.common import (
    get_dominant_items,
    unique_keep_order
)


def detect_dominant_topics(
    technology_frequency,
    methodology_frequency,
    domain_frequency
):

    dominant_topics = []

    for frequency_dict in [

        technology_frequency,

        methodology_frequency,

        domain_frequency

    ]:

        dominant_topics.extend(

            get_dominant_items(
                frequency_dict
            )
        )

    return unique_keep_order(
        dominant_topics
    )