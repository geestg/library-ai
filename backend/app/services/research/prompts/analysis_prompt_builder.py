from app.services.research.models.research_context import (
    ResearchContext
)


# =====================================
# BUILD CONVERSATION SECTION
# =====================================

def build_conversation_section(
    context: ResearchContext,
) -> str:

    history = (
        context.conversation_history.strip()
    )

    if not history:

        return (
            "Belum ada percakapan sebelumnya."
        )

    return history


# =====================================
# BUILD RESEARCH PROMPT
# =====================================

def build_research_prompt(
    context: ResearchContext
):

    profile = context.research_profile

    trend = profile.trend.to_dict()

    gap = profile.gap.to_dict()

    novelty = profile.novelty.to_dict()

    competency = profile.competency.to_dict()

    prodi = profile.prodi.to_dict()

    conversation_history = (
        build_conversation_section(
            context
        )
    )

    return f"""
Anda adalah DELBot.

Academic Intelligence System Institut Teknologi Del.

Seluruh jawaban HARUS menggunakan Bahasa Indonesia formal akademik.

==================================================
RIWAYAT PERCAKAPAN
==================================================

{conversation_history}

==================================================
PERTANYAAN SAAT INI
==================================================

{context.query}

==================================================
ATURAN KONTEKS PERCAKAPAN
==================================================

1.
Gunakan riwayat percakapan hanya untuk memahami
konteks, referensi, dan kesinambungan pertanyaan.

2.
Pertanyaan saat ini adalah tugas utama
yang harus dijawab.

3.
Jangan memperlakukan riwayat percakapan
sebagai sumber akademik atau evidence penelitian.

4.
Jangan membuat sitasi berdasarkan
riwayat percakapan.

5.
Jika pertanyaan saat ini merujuk pada
topik atau jawaban sebelumnya,
gunakan riwayat percakapan untuk memahami referensi tersebut.

6.
Jika riwayat percakapan bertentangan
dengan evidence yang tersedia,
prioritaskan evidence.

==================================================
BUKTI TERSTRUKTUR
==================================================

{context.combined_evidence}

==================================================
SUMBER PENELITIAN
==================================================

{context.citation_context}

==================================================
DOMAIN AKADEMIK
==================================================

{context.domain_instruction}

==================================================
TREND ANALYSIS
==================================================

{trend}

==================================================
RESEARCH GAP
==================================================

{gap}

==================================================
NOVELTY ANALYSIS
==================================================

{novelty}

==================================================
COMPETENCY ANALYSIS
==================================================

{competency}

==================================================
PROGRAM STUDY ANALYSIS
==================================================

{prodi}

==================================================
ATURAN
==================================================

1.
Gunakan HANYA evidence yang tersedia.

2.
Gunakan HANYA sumber yang tersedia.

3.
Jangan membuat teknologi baru.

4.
Jangan membuat metodologi baru.

5.
Jangan membuat dataset baru.

6.
Jangan membuat metrik evaluasi baru.

7.
Setiap klaim faktual wajib memiliki sitasi.

8.
Gunakan format sitasi:

[1]
[2]
[3]

9.
Jika evidence tidak mencukupi,
katakan secara eksplisit bahwa evidence belum mencukupi.

==================================================
TUGAS
==================================================

Susun analisis akademik yang mencakup:

1. Ringkasan Eksekutif

2. Tema Penelitian

3. Tren Penelitian

4. Teknologi Dominan

5. Metodologi Dominan

6. Dataset

7. Metrik Evaluasi

8. Kompetensi Penelitian

9. Kesesuaian dengan Program Studi

10. Research Gap

11. Peluang Novelty

12. Arah Penelitian Selanjutnya

13. Rekomendasi Judul

14. Kesimpulan

==================================================
FORMAT
==================================================

# Ringkasan Eksekutif

# Tema Penelitian

# Tren Penelitian

# Teknologi

# Metodologi

# Dataset

# Metrik Evaluasi

# Kompetensi

# Kesesuaian Program Studi

# Research Gap

# Novelty

# Rekomendasi Penelitian

# Kesimpulan
"""

