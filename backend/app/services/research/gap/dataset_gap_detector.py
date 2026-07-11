from app.services.research.gap.common import (
    get_sorted_items,
    get_top_item
)


# =====================================
# DATASET GAP DETECTOR
# =====================================

DOMINANT_THRESHOLD = 3


def detect_dataset_gap(
    dataset_frequency
):

    if not dataset_frequency:

        return [

            "Bukti penggunaan dataset masih sangat terbatas."
        ]

    sorted_datasets = (
        get_sorted_items(
            dataset_frequency
        )
    )

    top_dataset = (
        get_top_item(
            dataset_frequency
        )
    )

    gaps = []

    # =================================
    # NO DOMINANT DATASET
    # =================================

    if (

        top_dataset is None

        or

        top_dataset[1] < DOMINANT_THRESHOLD

    ):

        gaps.append(

            "Belum terdapat dataset yang benar-benar dominan sehingga eksplorasi dataset alternatif masih sangat terbuka."
        )

    # =================================
    # RARE DATASET
    # =================================

    for dataset, count in sorted_datasets:

        if count > 1:

            continue

        gaps.append(

            f"Dataset '{dataset}' masih sangat jarang digunakan sehingga memiliki peluang penelitian lebih lanjut."
        )

    return gaps
