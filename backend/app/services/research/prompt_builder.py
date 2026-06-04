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

    # =================================
    # RESEARCH DOMAINS
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

    return "\n".join(
        lines
    )


# =====================================
# BUILD EVIDENCE MATRIX
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
    # TECHNOLOGY FREQUENCY
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
    # METHODOLOGY FREQUENCY
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
    # DOMAIN FREQUENCY
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

    return "\n".join(
        lines
    )


# =====================================
# RESEARCH ANALYSIS PROMPT
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
BUKTI TERSTRUKTUR
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

4. Nama teknologi tetap menggunakan nama asli:
   - Laravel
   - API
   - Odoo
   - CNN
   - Transformer
   - React
   - FastAPI
   - Qdrant

5. Jangan menerjemahkan nama teknologi.

6. Seluruh analisis, penjelasan,
   rekomendasi, dan kesimpulan
   harus menggunakan Bahasa Indonesia.

==================================================
ATURAN GROUNDING
==================================================

1. Gunakan HANYA sumber yang ditemukan.

2. Gunakan HANYA teknologi yang
   terdapat pada bukti terstruktur.

3. Gunakan HANYA metodologi yang
   terdapat pada bukti terstruktur.

4. Jangan mengarang:

   - model AI
   - framework
   - arsitektur
   - teknologi
   - dataset
   - metodologi

5. Jika informasi tidak tersedia,
   tulis:

   "Bukti dari skripsi yang ditemukan tidak mencukupi."

6. Setiap klaim faktual
   wajib memiliki sitasi.

7. Format sitasi:

   [1]
   [2]
   [3]

8. Jangan gunakan:

   (Source_1)
   (Source_2)

==================================================
ATURAN STATISTIK
==================================================

Teknologi atau metodologi
dengan frekuensi = 1

TIDAK BOLEH disebut:

- dominan
- umum digunakan
- tren utama
- banyak digunakan

Teknologi atau metodologi
dengan frekuensi >= 2

boleh disebut tren.

Teknologi atau metodologi
dengan frekuensi >= 3

boleh disebut dominan.

==================================================
TUGAS ANALISIS
==================================================

1. Ringkasan Eksekutif
2. Tema Penelitian
3. Teknologi yang Digunakan
4. Metodologi yang Digunakan
5. Kelemahan Penelitian Sebelumnya
6. Gap Penelitian
7. Peluang Novelty
8. Arah Penelitian Selanjutnya
9. Rekomendasi Judul Skripsi
10. Rekomendasi Akhir

==================================================
FORMAT OUTPUT
==================================================

# Ringkasan Eksekutif

# Tema Penelitian

# Teknologi yang Digunakan

# Metodologi yang Digunakan

# Kelemahan Penelitian Sebelumnya

# Gap Penelitian

# Peluang Novelty

# Arah Penelitian Selanjutnya

# Rekomendasi Judul Skripsi

# Rekomendasi Akhir
"""