def detect_method_gap(
    methodology_frequency: dict
):

    gaps = []

    if not methodology_frequency:

        return [

            "Informasi metodologi penelitian belum mencukupi untuk dianalisis."
        ]

    sorted_methods = sorted(

        methodology_frequency.items(),

        key=lambda x: x[1],

        reverse=True
    )

    dominant_method = (
        sorted_methods[0][0]
    )

    for method, count in sorted_methods[1:]:

        if count <= 1:

            gaps.append(

                f"Metodologi '{method}' masih jarang digunakan dibandingkan metodologi dominan '{dominant_method}'."
            )

    return gaps