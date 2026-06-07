# =====================================
# BUILD STRUCTURED EVIDENCE V2
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

    # =================================
    # TECHNOLOGIES
    # =================================

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

    # =================================
    # METHODOLOGIES
    # =================================

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

    # =================================
    # DOMAINS
    # =================================

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

    # =================================
    # DATASETS
    # =================================

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

    # =================================
    # EVALUATION METRICS
    # =================================

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

    # =================================
    # YEARS
    # =================================

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

    # =================================
    # KEYWORDS
    # =================================

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


# =====================================
# BUILD EVIDENCE MATRIX V2
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

    # =================================
    # TECHNOLOGY
    # =================================

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

    # =================================
    # METHODOLOGY
    # =================================

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

    # =================================
    # DOMAIN
    # =================================

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

    # =================================
    # DATASET
    # =================================

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

    # =================================
    # METRIC
    # =================================

    lines.append(
        "\nFREKUENSI METRIK EVALUASI:"
    )

    metric_frequency = matrix.get(
        "metric_frequency",
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

    # =================================
    # YEAR
    # =================================

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


# =====================================
# RESEARCH ANALYSIS PROMPT V2
# =====================================

def build_research_prompt(

    query: str,

    evidence_text: str,

    citation_context: str,

    mode: str = "analysis"
):

    return f"""
Anda adalah DELBot.

Asisten Riset Akademik Institut Teknologi Del.

Seluruh jawaban HARUS menggunakan Bahasa Indonesia formal akademik.

==================================================
TOPIK PENELITIAN
==================================================

{query}

==================================================
BUKTI TERSTRUKTUR DAN ANALISIS
==================================================

{evidence_text}

==================================================
SUMBER YANG DITEMUKAN
==================================================

{citation_context}

==================================================
ATURAN BAHASA
==================================================

1. Gunakan Bahasa Indonesia formal akademik.

2. Jangan menggunakan heading bahasa Inggris.

3. Jangan menggunakan paragraf bahasa Inggris.

4. Jangan menerjemahkan nama teknologi.

==================================================
ATURAN GROUNDING
==================================================

1. Gunakan HANYA sumber yang ditemukan.

2. Gunakan HANYA bukti yang terdapat pada bagian BUKTI TERSTRUKTUR.

3. Jangan mengarang:
   - teknologi
   - metodologi
   - dataset
   - framework
   - model AI
   - metrik evaluasi

4. Jika bukti tidak tersedia,
   tulis:

   "Bukti dari skripsi yang ditemukan tidak mencukupi."

5. Setiap klaim faktual wajib memiliki sitasi.

6. Gunakan format sitasi:

   [1]
   [2]
   [3]

==================================================
ATURAN ANALISIS
==================================================

Gunakan informasi berikut apabila tersedia:

- Teknologi dominan
- Metodologi dominan
- Domain dominan
- Dataset dominan
- Dataset yang jarang digunakan
- Metrik evaluasi yang digunakan
- Tahun penelitian terbaru
- Gap penelitian
- Peluang novelty

Jangan menyebut sesuatu sebagai tren
atau dominan jika frekuensinya rendah.

==================================================
TUGAS ANALISIS
==================================================

1. Ringkasan Eksekutif
2. Tema Penelitian
3. Teknologi yang Digunakan
4. Metodologi yang Digunakan
5. Dataset yang Digunakan
6. Metrik Evaluasi
7. Kelemahan Penelitian Sebelumnya
8. Gap Penelitian
9. Peluang Novelty
10. Arah Penelitian Selanjutnya
11. Rekomendasi Judul Skripsi
12. Rekomendasi Akhir

==================================================
FORMAT OUTPUT
==================================================

# Ringkasan Eksekutif

# Tema Penelitian

# Teknologi yang Digunakan

# Metodologi yang Digunakan

# Dataset yang Digunakan

# Metrik Evaluasi

# Kelemahan Penelitian Sebelumnya

# Gap Penelitian

# Peluang Novelty

# Arah Penelitian Selanjutnya

# Rekomendasi Judul Skripsi

# Rekomendasi Akhir
"""