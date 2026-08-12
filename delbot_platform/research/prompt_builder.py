from __future__ import annotations

from typing import Any


class ResearchPromptBuilder:

    def build(
        self,
        *,
        query: str,
        context: str,
        history: list[dict] | None = None,
        previous: str = "",
        research_state: dict[str, Any] | None = None,
        mode: str = "research",
    ) -> list[dict]:

        messages: list[dict] = []

        history = history or []
        research_state = research_state or {}

        if mode in ("conversation", "discovery"):

            system_content = (
                "Anda adalah DELBot.\n\n"
                "Anda adalah AI Research Assistant yang juga mampu "
                "berbicara secara natural.\n\n"
                "MODE: CONVERSATION\n"
                "1. Jawab sapaan dan percakapan ringan secara natural, "
                "ramah, singkat, dan manusiawi.\n"
                "2. Gunakan history dan previous answer agar percakapan "
                "tetap nyambung.\n"
                "3. Jangan memaksakan dokumen, sitasi, research gap, "
                "atau thesis idea jika pengguna belum membahas penelitian.\n"
                "4. Jika pengguna mulai membahas penelitian, bantu "
                "mempersempit topik dan arah penelitian secara natural.\n"
                "5. Jika pengguna memberikan topik yang terlalu luas, "
                "tanyakan atau sarankan beberapa ranah yang lebih spesifik.\n"
                "6. Jangan membuat fakta akademik atau sitasi palsu.\n"
                "7. Tetap gunakan bahasa Indonesia yang natural dan "
                "tidak kaku, tetapi tetap sopan dan akademik ketika "
                "pembicaraan mulai masuk ke penelitian.\n"
            )

        else:

            system_content = (
                "Anda adalah DELBot.\n\n"
                "Anda adalah AI Research Assistant akademik.\n\n"
                "MODE: RESEARCH\n"
                "Aturan utama:\n"
                "1. Gunakan informasi dari context dokumen yang diberikan.\n"
                "2. Jangan membuat sitasi atau fakta yang tidak didukung context.\n"
                "3. Abaikan daftar isi, daftar gambar, daftar tabel, "
                "daftar lampiran, bibliografi, nomor halaman, dan "
                "navigation text sebagai evidence.\n"
                "4. Gunakan bagian substantif seperti masalah penelitian, "
                "tujuan, metode, hasil, temuan, pembahasan, keterbatasan, "
                "rekomendasi, dan future work.\n"
                "5. Jika context berisi campuran navigation text dan "
                "evidence substantif, gunakan evidence substantif yang tersedia.\n"
                "6. Untuk research gap, identifikasi keterbatasan, aspek "
                "yang belum dibahas, perbedaan pendekatan, atau peluang "
                "penelitian yang benar-benar didukung context.\n"
                "7. Untuk thesis idea, turunkan ide dari masalah, "
                "keterbatasan, metode, hasil, atau rekomendasi yang "
                "ditemukan dalam context.\n"
                "8. Bedakan fakta dari inference. Tandai inference "
                "sebagai kemungkinan atau arah penelitian.\n"
                "9. Jangan merangkum seluruh dokumen jika pertanyaan "
                "meminta gap atau thesis idea.\n"
                "10. Jika evidence substantif benar-benar tidak tersedia, "
                "nyatakan evidence belum memadai.\n"
                "11. Jika evidence substantif tersedia, jangan menolak "
                "menjawab hanya karena context juga mengandung navigation text.\n"
                "12. Jawaban harus akademik, objektif, ringkas, dan terstruktur.\n"
                "13. Untuk pertanyaan penelitian yang terlalu luas, "
                "bantu pengguna mempersempit bidang, objek, masalah, "
                "metode, atau konteks penelitian.\n"
                "14. Thesis idea harus diturunkan dari evidence dan "
                "research gap yang ditemukan, bukan ide generik yang "
                "tidak berhubungan dengan dokumen.\n"
                "15. Research gap harus mempunyai hubungan yang jelas "
                "dengan evidence dari dataset.\n"
                "16. Thesis idea harus menjelaskan masalah, gap, arah "
                "solusi atau penelitian, dan alasan mengapa ide tersebut "
                "relevan berdasarkan evidence.\n"
            )

        messages.append(
            {
                "role": "system",
                "content": system_content,
            }
        )

        if research_state:

            topic = research_state.get("topic")
            goal = research_state.get("research_goal")
            direction = research_state.get(
                "research_direction"
            )
            summary = research_state.get("summary")
            gap = research_state.get(
                "research_gap"
            )
            thesis_idea = research_state.get(
                "thesis_idea"
            )
            keywords = research_state.get(
                "keywords",
                [],
            )
            sources = research_state.get(
                "sources",
                [],
            )

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "CURRENT RESEARCH STATE\n\n"
                        f"Topic:\n{topic}\n\n"
                        f"Goal:\n{goal}\n\n"
                        f"Research Direction:\n{direction}\n\n"
                        f"Summary:\n{summary}\n\n"
                        f"Research Gap:\n{gap}\n\n"
                        f"Thesis Idea:\n{thesis_idea}\n\n"
                        f"Keywords:\n{keywords}\n\n"
                        f"Known Sources:\n{sources}"
                    ),
                }
            )

        if mode in ("research", "discovery"):

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "DOCUMENT CONTEXT\n\n"
                        f"{context}"
                    ),
                }
            )

        if previous:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "PREVIOUS ANSWER\n\n"
                        f"{previous}"
                    ),
                }
            )

        if history:

            messages.extend(
                history[-8:]
            )

        messages.append(
            {
                "role": "user",
                "content": query,
            }
        )

        return messages
