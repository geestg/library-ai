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
                "MODE: CONVERSATION / DISCOVERY\n"
                "Aturan:\n"
                "1. Jawab pertanyaan pengguna secara langsung.\n"
                "2. Gunakan history dan previous answer agar percakapan "
                "tetap nyambung.\n"
                "3. Gunakan context hanya sebagai informasi pendukung.\n"
                "4. Jangan menyalin context mentah ke dalam jawaban.\n"
                "5. Jangan membuat fakta atau sitasi palsu.\n"
                "6. Untuk discovery, jelaskan kandidat dokumen secara "
                "ringkas berdasarkan metadata/abstract yang tersedia.\n"
                "7. Jangan menganggap metadata atau abstract sebagai "
                "fulltext atau evidence halaman/section.\n"
                "8. Jika pengguna mulai membahas penelitian, bantu "
                "mempersempit topik dan arah penelitian.\n"
                "9. Jika topik terlalu luas, bantu mempersempit bidang, "
                "objek, masalah, metode, atau konteks.\n"
                "10. Gunakan bahasa Indonesia yang natural, jelas, dan "
                "ringkas.\n"
            )

        else:

            system_content = (
                "Anda adalah DELBot.\n\n"
                "Anda adalah AI Research Assistant akademik.\n\n"
                "MODE: RESEARCH\n\n"

                "TUJUAN OUTPUT:\n"
                "Berikan jawaban akademik yang merupakan SINTESIS dari "
                "evidence yang relevan untuk menjawab pertanyaan pengguna.\n\n"

                "ATURAN EVIDENCE:\n"
                "1. Gunakan hanya informasi yang didukung oleh context.\n"
                "2. Prioritaskan evidence substantif dari fulltext.\n"
                "3. Abstract metadata boleh digunakan sebagai evidence "
                "terbatas jika fulltext tidak tersedia.\n"
                "4. Metadata/abstract tidak boleh dianggap sebagai "
                "evidence halaman atau section PDF.\n"
                "5. Jika evidence tidak memadai, nyatakan secara jelas "
                "bahwa evidence yang tersedia belum cukup.\n"
                "6. Jangan membuat fakta, sumber, halaman, section, "
                "atau sitasi yang tidak diberikan.\n"
                "7. Bedakan fakta dari inference. Inference harus "
                "dinyatakan sebagai kemungkinan atau arah penelitian.\n\n"

                "ATURAN CONTEXT:\n"
                "8. Context adalah bahan sumber, BUKAN teks yang harus "
                "disalin kembali.\n"
                "9. Jangan menyalin context secara panjang atau mentah.\n"
                "10. Jangan mengulang daftar dokumen, metadata, daftar "
                "isi, navigation text, bibliografi, atau nomor halaman "
                "kecuali memang diperlukan untuk menjawab pertanyaan.\n"
                "11. Jangan memulai jawaban dengan kalimat generik seperti "
                "\"Berdasarkan dokumen yang ditemukan\" lalu menyalin "
                "isi context.\n"
                "12. Ekstrak informasi yang relevan, gabungkan evidence "
                "yang saling mendukung, lalu tulis ulang dengan kata-kata "
                "sendiri.\n\n"

                "ATURAN ANSWER:\n"
                "13. Jawab inti pertanyaan pada kalimat atau paragraf "
                "pertama.\n"
                "14. Jawaban harus ringkas dan proporsional terhadap "
                "pertanyaan.\n"
                "15. Untuk pertanyaan definisi atau fakta sederhana, "
                "cukup 1-3 paragraf pendek.\n"
                "16. Untuk pertanyaan metode, hasil, atau perbandingan, "
                "gunakan poin-poin hanya jika membantu keterbacaan.\n"
                "17. Jangan merangkum seluruh dokumen jika pengguna "
                "menanyakan satu hal spesifik.\n"
                "18. Jangan mengulang pertanyaan pengguna.\n"
                "19. Jangan menambahkan kesimpulan panjang yang tidak "
                "diminta.\n"
                "20. Jangan membuat jawaban lebih panjang hanya karena "
                "context yang tersedia panjang.\n\n"

                "RESEARCH GAP:\n"
                "21. Research gap harus diturunkan dari keterbatasan, "
                "aspek yang belum dibahas, perbedaan pendekatan, atau "
                "peluang penelitian yang benar-benar didukung evidence.\n"
                "22. Jangan menghasilkan research gap generik yang tidak "
                "mempunyai hubungan jelas dengan dokumen.\n\n"

                "THESIS IDEA:\n"
                "23. Thesis idea harus diturunkan dari evidence dan "
                "research gap.\n"
                "24. Jelaskan secara ringkas masalah, gap, arah penelitian "
                "atau metode yang mungkin, dan alasan relevansinya.\n"
                "25. Jangan memberikan ide penelitian generik yang tidak "
                "berhubungan dengan evidence.\n\n"

            # GROUNDED_THESIS_SYNTHESIS_767799
            "THESIS SYNTHESIS GROUNDED:\n"
            "Jika pengguna meminta thesis ideas dan context memuat dua atau lebih evidence yang relevan, jangan menolak seluruh permintaan hanya karena fulltext atau detail tertentu terbatas.\n"
            "Susun tepat tiga ide menggunakan heading Ide 1, Ide 2, dan Ide 3.\n"
            "Untuk setiap ide jelaskan: masalah yang didukung evidence, research gap, metode yang diusulkan, rencana evaluasi, kontribusi, keterbatasan, dan sumber pendukung.\n"
            "Pisahkan fakta evidence dari proposal penelitian. Metode, evaluasi, dan kontribusi baru harus disebut sebagai usulan atau inference, bukan sebagai hasil studi terdahulu.\n"
            "Metadata abstract merupakan evidence terbatas yang sah untuk membangun arah ide ketika PDF tidak tersedia; nyatakan keterbatasannya tanpa menghentikan sintesis.\n"
            "Jangan membuat parameter, hasil, dataset, atau klaim eksperimen yang tidak tersedia dalam context.\n"
            "Jika sebagian detail belum tersedia, berikan rancangan evaluasi yang diusulkan dan tandai secara eksplisit sebagai proposal penelitian.\n\n"
                "FORMAT AKHIR:\n"
                "26. Output hanya jawaban untuk pengguna.\n"
                "27. Jangan menampilkan label internal seperti "
                "\"DOCUMENT CONTEXT\", \"PREVIOUS ANSWER\", atau "
                "\"CURRENT RESEARCH STATE\".\n"
                "28. Jangan menampilkan proses berpikir internal.\n"
                "29. Jangan mengarang citation marker. Citation sumber "
                "akan dikelola oleh sistem berdasarkan evidence yang "
                "ditemukan.\n"
                "30. Untuk pertanyaan definisi, pengertian, atau fakta "
                "sederhana, jawab langsung dalam 1-3 paragraf pendek.\n"
                "31. Jangan menyalin kalimat context secara berurutan. "
                "Sintesis harus ditulis ulang dengan kata-kata sendiri.\n"
                "32. Jangan memasukkan informasi yang tidak diperlukan "
                "untuk menjawab pertanyaan.\n"
                "33. Jika context memiliki banyak dokumen, gabungkan "
                "hanya evidence yang relevan dengan pertanyaan.\n"
                "34. Targetkan jawaban sekitar 80-250 kata untuk "
                "pertanyaan sederhana, kecuali pertanyaan memang "
                "memerlukan penjelasan lebih panjang.\n"
                "35. Sebelum mengakhiri jawaban, pastikan setiap bagian "
                "jawaban relevan terhadap pertanyaan pengguna dan "
                "bukan sekadar pengulangan context.\n"
                "36. Prioritaskan ketepatan, relevansi, dan keterbacaan "
                "daripada panjang jawaban.\n"
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
                        f"Known Sources:\n{sources}\n\n"
                        "Gunakan state ini hanya sebagai konteks "
                        "penelitian. Jangan menyalin state mentah "
                        "ke dalam jawaban."
                    ),
                }
            )

        if mode in ("research", "discovery"):

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "DOCUMENT CONTEXT\n\n"
                        f"{context}\n\n"
                        "Gunakan context di atas sebagai sumber informasi. "
                        "Jangan menyalinnya kembali. Pilih hanya evidence "
                        "yang relevan dengan pertanyaan pengguna."
                    ),
                }
            )

        if previous:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "PREVIOUS ANSWER\n\n"
                        f"{previous}\n\n"
                        "Gunakan previous answer hanya untuk menjaga "
                        "kontinuitas. Jangan menyalinnya kembali kecuali "
                        "bagian tersebut memang diperlukan untuk menjawab "
                        "pertanyaan terbaru."
                    ),
                }
            )

        if history:

            messages.extend(
                history[-8:]
            )

        if mode == "research":
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "FINAL ANSWER INSTRUCTION\n\n"
                        "Sekarang jawab pertanyaan pengguna secara langsung.\n"
                        "Gunakan context sebagai sumber evidence, tetapi "
                        "jangan menyalin context.\n"
                        "Untuk pertanyaan sederhana, berikan jawaban "
                        "singkat dan substantif.\n"
                        "Tulis sintesis dengan kata-kata sendiri.\n"
                        "Jangan memasukkan potongan dokumen yang tidak "
                        "menjawab pertanyaan.\n"
                        "Jika hanya sebagian informasi yang tersedia, "
                        "jawab berdasarkan bagian tersebut dan nyatakan "
                        "keterbatasannya bila relevan."
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": query,
            }
        )

        return messages
