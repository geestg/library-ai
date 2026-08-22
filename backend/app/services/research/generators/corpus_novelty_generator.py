from app.services.llm.model_gateway import gateway
from app.services.research.models.research_models import ResearchContext


def generate_corpus_novelty_check(context: ResearchContext) -> ResearchContext:
    """
    Generator respons investigasi status repositori skripsi IT Del & analisis kebaruan (Novelty Check).
    Menjawab pertanyaan user: "Apakah sudah ada skripsi IT Del yang meneliti X?"
    """
    profile = context.research_profile
    theses = context.theses or []

    # 1. KASUS A: DOKUMEN RELEVAN DITEMUKAN PADA REPOSITORI IT DEL (Theses >= 1)
    if theses:
        theses_str_list = []
        for idx, t in enumerate(theses, start=1):
            title = t.get('title', 'Untitled')
            author = t.get('author') or 'Unknown'
            year = t.get('year') or '-'
            prodi = t.get('prodi') or 'IT Del'
            abstract = t.get('abstract') or t.get('chunk') or ''
            methods = ", ".join(t.get('methodologies', [])) or "-"
            
            theses_str_list.append(
                f"[{idx}] Judul: {title}\n"
                f"    Penulis: {author} ({year}) | Program Studi: {prodi}\n"
                f"    Metode/Fokus: {methods}\n"
                f"    Ringkasan: {abstract[:400]}"
            )
        theses_str = "\n\n".join(theses_str_list)

        prompt = f"""Anda adalah DELBot, Academic Intelligence System & Research Advisor Institut Teknologi Del.

==================================================
PERTANYAAN INVESTIGASI REPOSITORI SKRIPSI
==================================================
"{context.query}"

==================================================
DOKUMEN RIIL DITEMUKAN DARI REPOSITORI IT DEL ({len(theses)} Dokumen):
==================================================
{theses_str}

==================================================
TUGAS UTAMA:
==================================================
1. Jawab pertanyaan user secara tegas bahwa **penelitian terkait topik tersebut SUDAH PERNAH DILAKUKAN** di repositori IT Del.
2. Paparkan ringkasan penelitian yang ditemukan (Judul, Penulis, Tahun, Prodi, dan Metode yang digunakan) dengan sitasi `[1]`, `[2]`. DILARANG KERAS mengarang nama peneliti di luar data di atas!
3. Jelaskan celah atau batasan yang belum diselesaikan oleh penelitian-penelitian terdahulu tersebut.
4. Berikan 2-3 rekomendasi peluang kebaruan (*novelty*) spesifik yang bisa dieksplorasi oleh mahasiswa berikutnya agar tidak terjadi duplikasi.

==================================================
FORMAT KELUARAN WAJIB (MARKDOWN):
==================================================
# Status Penelusuran Topik di Repositori IT Del

**Topik Analisis:** {context.query}

## 📌 Status Repositori
**Ya, penelitian mengenai/berkaitan dengan topik ini sudah pernah dilakukan di lingkungan Institut Teknologi Del.** Berdasarkan repositori skripsi yang terindeks, ditemukan {len(theses)} penelitian terdahulu yang relevan:

### 1. [Judul Skripsi 1] [1]
* **Penulis & Tahun:** [Nama Penulis] ([Tahun]) — Program Studi [Prodi]
* **Metode & Pendekatan:** [Ringkasan metode]
* **Fokus Penelitian:** [Uraian singkat kontribusi dokumen 1]

(Jika ada dokumen 2 atau 3, cantumkan dengan format yang sama)

---

## 🔍 Analisis Celah & Keterbatasan Penelitian Terdahulu
* [Jelaskan apa yang sudah dicakup oleh penelitian terdahulu di atas dan apa batasannya]

---

## 💡 Peluang Kebaruan (*Novelty Opportunity*)
Agar penelitian baru memiliki kontribusi yang berbeda dan tidak sekadar menduplikasi skripsi terdahulu, mahasiswa dapat mengeksplorasi:
1. **[Peluang Novelty 1]:** [Penjelasan usulan metode/dataset/domain baru]
2. **[Peluang Novelty 2]:** [Penjelasan usulan pengujian baru]
"""
        response_text = gateway.generate_response(prompt=prompt, max_tokens=1000)
    else:
        # 2. KASUS B: BELUM DITEMUKAN PADA HASIL RETRIEVAL REPOSITORI IT DEL (Theses == 0)
        response_text = f"""# Status Penelusuran Topik di Repositori IT Del

**Topik Analisis:** {context.query}

## 📌 Status Repositori
**Belum ditemukan.** Berdasarkan penelusuran pada korpus repositori skripsi Institut Teknologi Del yang terindeks saat ini, **belum ditemukan dokumen penelitian yang secara langsung membahas topik "{context.query}"**.

---

## 💡 Analisis Potensi Kebaruan (*Novelty Status*)
* **Status Validasi Kebaruan:** **Peluang Kebaruan Eksploratif (*Exploratory Novelty Opportunity*)**
* **Penjelasan Akademik:** Ketiadaan catatan penelitian terdahulu mengenai topik ini pada korpus repositori lokal yang ditelusuri menjadikan topik tersebut sebagai **peluang kebaruan yang sangat potensial**. Namun, status kebaruan definitif belum dapat divalidasi secara komparatif terhadap tugas akhir alumni IT Del karena ketiadaan data acuan pembanding pada repositori yang terindeks saat ini.

---

## 🎯 Rekomendasi Arah Penelitian (*Recommended Next Steps*)
1. **Studi Literatur Publikasi Eksternal:** Menelaah publikasi ilmiah internasional bereputasi (IEEE Xplore, ScienceDirect, ACM Digital Library) untuk memahami *state-of-the-art* (SOTA) metode dan dataset benchmark standar global.
2. **Kesesuaian dengan Kompetensi Prodi:** Menyelaraskan arsitektur teknis sistem dengan kurikulum dan profil keahlian program studi di IT Del.
3. **Pengumpulan Dataset Mandiri:** Menyiapkan data primer atau mengadaptasi dataset benchmark publik terverifikasi untuk kebutuhan implementasi awal."""

    context.analysis = response_text.strip()
    context.response = {
        "query": context.query,
        "ideas": response_text.strip(),
        "literature_review": response_text.strip(),
        "sources": context.theses,
        "citations": context.citations,
        "research_profile": profile.to_dict() if profile else {},
    }
    return context
