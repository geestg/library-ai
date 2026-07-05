from app.services.research.gap.common import (
    unique_keep_order
)


# =====================================
# NOVELTY OPPORTUNITY DETECTOR
# =====================================

def detect_novelty_opportunities(

    rare_topics,

    emerging_topics,

    dataset_frequency

):

    novelty = []

    # =================================
    # RARE TOPICS
    # =================================

    for topic in rare_topics:

        novelty.append(

            f"Topik '{topic}' masih sangat jarang diteliti sehingga berpotensi menjadi kontribusi penelitian yang lebih baru."
        )

    # =================================
    # RARE DATASETS
    # =================================

    for dataset, count in dataset_frequency.items():

        if count == 1:

            novelty.append(

                f"Pemanfaatan dataset '{dataset}' masih sangat terbatas sehingga layak dieksplorasi lebih lanjut."
            )

    # =================================
    # EMERGING TOPICS
    # =================================

    if emerging_topics:

        novelty.append(

            "Kombinasi topik emerging "

            + ", ".join(emerging_topics[:5])

            + " memiliki potensi menghasilkan penelitian yang lebih inovatif."
        )

    # =================================
    # NO NOVELTY FOUND
    # =================================

    if not novelty:

        novelty.append(

            "Belum ditemukan peluang novelty yang kuat berdasarkan evidence penelitian yang tersedia."
        )

    return unique_keep_order(
        novelty
    )