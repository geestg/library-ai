def detect_evaluation_gap(
    evaluation_frequency: dict
):

    gaps = []

    if not evaluation_frequency:

        return [

            "Sebagian besar penelitian tidak menyebutkan metrik evaluasi secara eksplisit."
        ]

    metric_count = len(
        evaluation_frequency
    )

    if metric_count <= 2:

        gaps.append(

            "Variasi metrik evaluasi masih terbatas sehingga peluang evaluasi yang lebih komprehensif masih terbuka."
        )

    metric_names = {

        metric.lower()

        for metric

        in evaluation_frequency.keys()
    }

    if (

        "accuracy" in metric_names

        and len(metric_names) == 1

    ):

        gaps.append(

            "Mayoritas penelitian hanya menggunakan Accuracy tanpa metrik tambahan seperti Precision, Recall, atau F1-Score."
        )

    return gaps
