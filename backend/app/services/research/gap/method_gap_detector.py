from app.services.research.gap.common import (
    get_sorted_items,
    get_top_item
)


# =====================================
# METHOD GAP DETECTOR
# =====================================

DOMINANT_THRESHOLD = 3


def detect_method_gap(
    methodology_frequency
):

    if not methodology_frequency:

        return [

            "Informasi metodologi penelitian belum mencukupi untuk dianalisis."
        ]

    sorted_methods = (
        get_sorted_items(
            methodology_frequency
        )
    )

    top_method = (
        get_top_item(
            methodology_frequency
        )
    )

    if top_method is None:

        return [

            "Informasi metodologi penelitian belum mencukupi untuk dianalisis."
        ]

    dominant_method = top_method[0]

    dominant_count = top_method[1]

    gaps = []

    # =================================
    # NO DOMINANT METHOD
    # =================================

    if dominant_count < DOMINANT_THRESHOLD:

        gaps.append(

            "Belum terdapat metodologi yang benar-benar dominan sehingga masih terbuka peluang eksplorasi berbagai pendekatan penelitian."
        )

    # =================================
    # RARE METHODS
    # =================================

    for method, count in sorted_methods:

        if count > 1:

            continue

        gaps.append(

            f"Metodologi '{method}' masih sangat jarang digunakan sehingga memiliki peluang untuk dieksplorasi lebih lanjut."
        )

    return gaps

