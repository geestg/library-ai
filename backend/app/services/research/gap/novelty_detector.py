from app.services.research.gap.common import (
    unique_keep_order
)


def detect_novelty_opportunities(

    rare_topics,

    emerging_topics,

    dataset_frequency

):

    novelty = []

    for topic in rare_topics:

        novelty.append(

            f"Eksplorasi lebih lanjut pada topik '{topic}' berpotensi menghasilkan kontribusi penelitian yang lebih baru dibandingkan area yang sudah dominan."
        )

    for dataset, count in dataset_frequency.items():

        if count == 1:

            novelty.append(

                f"Penggunaan dataset '{dataset}' dapat menjadi peluang novelty karena masih jarang ditemukan."
            )

    if emerging_topics:

        novelty.append(

            f"Kombinasi topik emerging seperti {', '.join(emerging_topics[:3])} berpotensi menghasilkan kontribusi penelitian yang lebih unik."
        )

    return unique_keep_order(
        novelty
    )