from app.services.prompts.composer import (
    PromptComposer,
)


class QueryResolutionPrompt:

    @staticmethod
    def build(
        *,
        query: str,
        conversation_history: str,
    ) -> str:

        intro = f"""
Anda adalah query resolver untuk sistem research
dan document retrieval.

Tugas Anda adalah mengubah pertanyaan terbaru user
menjadi pertanyaan mandiri yang dapat dipahami tanpa
harus membaca percakapan sebelumnya.

==================================================
RIWAYAT PERCAKAPAN SEBELUM PERTANYAAN TERBARU
==================================================

{conversation_history}

==================================================
PERTANYAAN TERBARU USER
==================================================

{query}
""".strip()

        rules = """
==================================================
ATURAN
==================================================

1. Gunakan riwayat percakapan hanya untuk
menyelesaikan referensi yang ambigu.

2. Referensi ambigu dapat berupa:
"keduanya", "ketiganya", "ini", "itu",
"tersebut", "yang pertama", "yang kedua",
"yang tadi", "bagaimana dengan yang lain",
atau referensi kontekstual serupa.

3. Pertahankan maksud asli pertanyaan user.

4. Jangan menjawab pertanyaan.

5. Jangan menambahkan fakta baru.

6. Jangan menggunakan pengetahuan eksternal.

7. Jangan membuat asumsi yang tidak didukung
oleh riwayat percakapan.

8. Jika pertanyaan terbaru sudah mandiri,
kembalikan pertanyaan tersebut tanpa perubahan.

9. Output hanya satu pertanyaan hasil resolusi.

10. Jangan menambahkan penjelasan,
label, Markdown, tanda kutip,
atau teks lain.
""".strip()

        output = """
==================================================
OUTPUT
==================================================

Kembalikan hanya pertanyaan mandiri.
""".strip()

        return PromptComposer.compose(

            intro,

            rules,

            output,

        )