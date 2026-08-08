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
    ) -> list[dict]:

        messages: list[dict] = []

        messages.append(
            {
                "role": "system",
                "content": (
                    "Anda adalah DELBot.\n\n"
                    "Anda adalah AI Research Assistant akademik.\n\n"
                    "Aturan utama:\n"
                    "1. Gunakan informasi dari context dokumen yang diberikan.\n"
                    "2. Jangan membuat sitasi atau fakta yang tidak didukung context.\n"
                    "3. Abaikan daftar isi, daftar gambar, daftar tabel, daftar lampiran, "
                    "bibliografi, nomor halaman, dan navigation text sebagai evidence.\n"
                    "4. Gunakan bagian substantif seperti masalah penelitian, tujuan, metode, "
                    "hasil, temuan, pembahasan, keterbatasan, rekomendasi, dan future work.\n"
                    "5. Jika context berisi campuran navigation text dan evidence substantif, "
                    "gunakan evidence substantif yang tersedia.\n"
                    "6. Untuk research gap, identifikasi keterbatasan, aspek yang belum dibahas, "
                    "perbedaan pendekatan, atau peluang penelitian yang benar-benar didukung context.\n"
                    "7. Untuk thesis idea, turunkan ide dari masalah, keterbatasan, metode, "
                    "hasil, atau rekomendasi yang ditemukan dalam context.\n"
                    "8. Bedakan fakta dari inference. Tandai inference sebagai kemungkinan atau arah penelitian.\n"
                    "9. Jangan merangkum seluruh dokumen jika pertanyaan meminta gap atau thesis idea.\n"
                    "10. Jika evidence substantif benar-benar tidak tersedia, nyatakan evidence belum memadai.\n"
                    "11. Jika evidence substantif tersedia, jangan menolak menjawab hanya karena context "
                    "juga mengandung navigation text.\n"
                    "12. Jawaban harus akademik, objektif, ringkas, dan terstruktur."
                ),
            }
        )

        if research_state:

            topic = research_state.get("topic")
            goal = research_state.get("research_goal")
            summary = research_state.get("summary")
            keywords = research_state.get("keywords", [])
            sources = research_state.get("sources", [])

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "CURRENT RESEARCH STATE\n\n"
                        f"Topic:\n{topic}\n\n"
                        f"Goal:\n{goal}\n\n"
                        f"Summary:\n{summary}\n\n"
                        f"Keywords:\n{keywords}\n\n"
                        f"Known Sources:\n{sources}"
                    ),
                }
            )

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

            messages.extend(history[-5:])

        messages.append(
            {
                "role": "user",
                "content": query,
            }
        )

        return messages