def detect_dataset_gap(
    dataset_frequency: dict
):

    gaps = []

    if not dataset_frequency:

        return [

            "Bukti penggunaan dataset masih sangat terbatas."
        ]

    sorted_datasets = sorted(

        dataset_frequency.items(),

        key=lambda x: x[1],

        reverse=True
    )

    dominant_dataset = (
        sorted_datasets[0][0]
    )

    for dataset, count in sorted_datasets:

        if count == 1:

            gaps.append(

                f"Dataset '{dataset}' masih sangat sedikit digunakan dibandingkan dataset dominan '{dominant_dataset}'."
            )

    return gaps