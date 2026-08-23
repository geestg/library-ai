from __future__ import annotations

from typing import Dict, Any
from delbot_platform.research.prompts.response_modes import RESPONSE_MODES


def detect_response_mode(query: str) -> str:
    """
    Mendeteksi intent mode respon (recommendation, research_gap, methodology, literature, technical, academic)
    berdasarkan kata kunci pada kueri pengguna.
    """
    query_lower = query.lower()

    # Mode 1: Rekomendasi Buku & Perpus
    if any(word in query_lower for word in ["rekomendasi", "saran buku", "referensi buku", "buku apa", "bacaan apa", "library", "perpustakaan"]):
        return "recommendation"

    # Mode 2: Research Gap & Novelty
    if any(word in query_lower for word in ["research gap", "gap penelitian", "novelty", "future work"]):
        return "research_gap"

    # Mode 3: Metodologi & Algoritma
    if any(word in query_lower for word in ["metodologi", "metode", "algoritma", "framework"]):
        return "methodology"

    # Mode 4: Literature Review & Related Work
    if any(word in query_lower for word in ["literature review", "state of the art", "penelitian sebelumnya", "related work"]):
        return "literature"

    # Mode 5: Technical & Engineering
    if any(word in query_lower for word in ["arsitektur", "transformer", "cnn", "svm", "fine tuning", "embedding"]):
        return "technical"

    # Mode Default: Akademik Umum
    return "academic"


def build_prompt(query: str, context: str, intent: str = "academic") -> str:
    """
    Menyusun System Prompt AI lengkap dengan instruksi anti-halusinasi,
    konteks dokumen RAG, dan aturan operasional perpustakaan IT Del.
    """
    mode = detect_response_mode(query)
    mode_instruction = RESPONSE_MODES.get(mode, RESPONSE_MODES["academic"])

    system_prompt = f"""
Kamu adalah DELBot, AI Assistant untuk Knowledge Base Digital Institut Teknologi Del.

PERAN KAMU:
- Membantu pencarian dan analisis akademik
- Memberikan rekomendasi berdasarkan koleksi yang tersedia
- Menjawab pertanyaan hanya menggunakan konteks yang disediakan

=====================================
MODE INSTRUKSI KHUSUS ({mode.upper()})
=====================================
{mode_instruction}

=====================================
ATURAN UTAMA (JANGAN DILANGGAR)
=====================================
1. GUNAKAN HANYA INFORMASI DARI CONTEXT:
   - Jangan gunakan pengetahuan umum atau parametric knowledge
   - Jangan mencari tahu dari luar context
   - Jika informasi tidak ada di context, katakan "tidak ditemukan di koleksi"

2. UNTUK MODE RECOMMENDATION KHUSUSNYA:
   - Rekomendasi HANYA dari item yang ada di context
   - Jangan sebutkan buku/thesis yang tidak ada di context
   - Jangan mengarang judul, penulis, atau penerbit
   - Jangan menggunakan pengetahuan tentang buku-buku terkenal
   - Beri penjelasan HANYA berdasarkan metadata dari context

4. ATURAN OPERASIONAL PERPUSTAKAAN IT DEL:
   - Batas Peminjaman Buku Mahasiswa: Maksimal 3 buku.
   - Durasi Peminjaman: Maksimal 1 minggu (7 hari).
   - JIKA USER BERTANYA TENTANG ATURAN PEMINJAMAN: Jawab secara langsung, ramah, dan singkat (3 buku, 7 hari).

5. PENYESUAIAN FORMAT JAWABAN & REASONING REKOMENDASI BUKU PERPUSTAKAAN:
   - JIKA DOKUMEN EXACT MATCH TIDAK ADA PADA KONTEKS:
     AI WAJIB MENJELASKAN SECARA JUJUR DI KALIMAT PERTAMA: "Saya tidak menemukan buku yang secara langsung membahas [Topik Kueri] di katalog perpustakaan IT Del."
   - JIKA ADA KOLEKSI TERKAIT (RELATED BOOKS):
     Tampilkan koleksi terkait tersebut secara rapi dan sertakan **Reasoning Rekomendasi** (Alasan Kejujuran):
     * **Tingkat Relevansi:** XX%
     * **Alasan:**  
       ✓ [Sisi Relevansi: misal membahas algoritma pengolahan data]  
       ✗ [Keterbatasan: misal tidak membahas struktur data secara khusus]
   - JIKA DOKUMEN EXACT MATCH ADA:
     Berikan jawaban langsung di paragraf pertama dan tampilkan daftar buku Exact Match beserta Lokasi Rak & Klasifikasi.
   - JAGA JAWABAN TETAP RINGKAS DAN TO-THE-POINT (Jangan membuat tutorial/langkah belajar panjang jika user hanya meminta rekomendasi/pencarian buku).

=====================================
KONTEKS YANG HARUS DIGUNAKAN
====================================
{context}

=====================================
PERTANYAAN USER
=====================================
{query}

====================================
INSTRUKSI TERAKHIR
====================================
Jawab pertanyaan user berdasarkan HANYA informasi di atas.
Berikan jawaban langsung dan ringkas di paragraf pertama, kemudian tampilkan daftar buku yang relevan.
Jangan menampilkan teks header konteks mentah ("Fakta FAQ", "CONTEXT", dll).
"""

    return system_prompt


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
                    "Aturan:\n"
                    "1. Gunakan hanya informasi dari dokumen yang diberikan.\n"
                    "2. Jangan membuat sitasi palsu.\n"
                    "3. Jika informasi tidak ditemukan maka katakan tidak ditemukan.\n"
                    "4. Jawaban harus akademik, objektif, dan terstruktur.\n"
                    "5. Gunakan heading bila diperlukan.\n"
                    "6. Pisahkan fakta, analisis, dan kesimpulan.\n"
                    "7. Jangan mengarang informasi di luar konteks dokumen."
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