# =====================================
# BUILD MATRIX SECTION
# =====================================

def build_matrix_section(
    matrix: dict
):

    lines = []

    lines.append(
        "MATRIKS BUKTI"
    )

    lines.append(
        "=" * 50
    )

    lines.append(
        "\nFREKUENSI TEKNOLOGI:"
    )

    technology_frequency = matrix.get(
        "technology_frequency",
        {}
    )

    if technology_frequency:

        for name, count in technology_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nFREKUENSI METODOLOGI:"
    )

    methodology_frequency = matrix.get(
        "methodology_frequency",
        {}
    )

    if methodology_frequency:

        for name, count in methodology_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nFREKUENSI DOMAIN:"
    )

    domain_frequency = matrix.get(
        "domain_frequency",
        {}
    )

    if domain_frequency:

        for name, count in domain_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nFREKUENSI DATASET:"
    )

    dataset_frequency = matrix.get(
        "dataset_frequency",
        {}
    )

    if dataset_frequency:

        for name, count in dataset_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nFREKUENSI METRIK EVALUASI:"
    )

    metric_frequency = matrix.get(
        "evaluation_frequency",
        {}
    )

    if metric_frequency:

        for name, count in metric_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nFREKUENSI TAHUN PENELITIAN:"
    )

    year_frequency = matrix.get(
        "year_frequency",
        {}
    )

    if year_frequency:

        for name, count in year_frequency.items():

            lines.append(
                f"- {name} ({count})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    return "\n".join(
        lines
    )

