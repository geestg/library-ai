def build_comparison_table(
    comparison_result: dict
):

    methods = comparison_result.get(
        "methods",
        []
    )

    if not methods:

        return (
            "Tidak ada metode yang "
            "dapat dibandingkan."
        )

    lines = []

    lines.append(
        "| Method | Frequency | Interpretability | Complexity |"
    )

    lines.append(
        "|----------|----------|----------|----------|"
    )

    for item in methods:

        lines.append(

            f"| {item['method']} "

            f"| {item['frequency']} "

            f"| {item['interpretability']} "

            f"| {item['complexity']} |"
        )

    return "\n".join(
        lines
    )

