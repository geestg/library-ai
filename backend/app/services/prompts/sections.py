# =====================================
# COMMON PROMPT SECTIONS
# =====================================

LANGUAGE_RULES = """
==================================================
FORMAT
==================================================

1. Gunakan Bahasa Indonesia.

2. Gunakan Markdown murni.

3. Jangan gunakan tag HTML.

4. Jangan membuat heading jika jawaban cukup
disampaikan dalam satu atau dua kalimat.

5. Jangan membuat tabel kecuali struktur
pertanyaan memang membutuhkannya.

6. Gunakan jawaban sesingkat mungkin tanpa
menghilangkan fakta relevan.
""".strip()


GROUNDING_RULES = """
==================================================
PRINSIP UTAMA
==================================================

Gunakan hanya informasi yang tersedia
pada konteks.

Jangan menggunakan:

- pengetahuan eksternal
- asumsi
- tebakan
- halusinasi
- informasi yang tidak tersedia

Semua klaim harus dapat didukung
oleh konteks yang diberikan.
""".strip()


NO_INTERNAL_REASONING = """
==================================================
LARANGAN
==================================================

Jangan menyebut:

- prompt
- pipeline
- retrieval
- chunk
- evidence
- verifier
- context window
- model
- similarity score

Sampaikan hasilnya langsung
kepada pengguna.
""".strip()