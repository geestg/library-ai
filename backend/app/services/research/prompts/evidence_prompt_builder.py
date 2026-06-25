# =====================================
# BUILD STRUCTURED EVIDENCE
# =====================================

def build_evidence_section(
    evidence: dict
):

    technologies = evidence.get(
        "technologies",
        []
    )

    methodologies = evidence.get(
        "methodologies",
        []
    )

    keywords = evidence.get(
        "keywords",
        []
    )

    research_domains = evidence.get(
        "research_domains",
        []
    )

    datasets = evidence.get(
        "datasets",
        []
    )

    evaluation_metrics = evidence.get(
        "evaluation_metrics",
        []
    )

    years = evidence.get(
        "years",
        []
    )

    lines = []

    lines.append(
        "BUKTI TERSTRUKTUR"
    )

    lines.append(
        "=" * 50
    )

    lines.append(
        "\nTEKNOLOGI:"
    )

    if technologies:

        for item in technologies:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nMETODOLOGI:"
    )

    if methodologies:

        for item in methodologies:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nDOMAIN PENELITIAN:"
    )

    if research_domains:

        for item in research_domains:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nDATASET:"
    )

    if datasets:

        for item in datasets:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nMETRIK EVALUASI:"
    )

    if evaluation_metrics:

        for item in evaluation_metrics:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nTAHUN PENELITIAN:"
    )

    if years:

        for item in years:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    lines.append(
        "\nKATA KUNCI:"
    )

    if keywords:

        for item in keywords[:20]:

            lines.append(
                f"- {item['name']} ({item['count']})"
            )

    else:

        lines.append(
            "- Tidak ditemukan"
        )

    return "\n".join(
        lines
    )