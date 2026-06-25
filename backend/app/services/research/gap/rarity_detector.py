from app.services.research.gap.common import (
    get_rare_items,
    unique_keep_order
)


def detect_rare_topics(
    technology_frequency,
    methodology_frequency,
    domain_frequency
):

    rare_topics = []

    for frequency_dict in [

        technology_frequency,

        methodology_frequency,

        domain_frequency

    ]:

        rare_topics.extend(

            get_rare_items(
                frequency_dict
            )
        )

    return unique_keep_order(
        rare_topics
    )