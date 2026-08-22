from app.services.llm.model_gateway import gateway
from app.services.research.models.research_models import ResearchContext


def generate_research_gap_report(context: ResearchContext) -> ResearchContext:
    """
    Generator Laporan Analisis Research Gap Akademik Berbasis Evidence Matrix & Claim Verification.
    Memisahkan secara ketat:
    1. FAKTA REPOSITORI (Evidence-grounded dari korpus lokal)
    2. INFERENSI CELAH (Research Gap berdasar keterbatasan rujukan)
    3. REKOMENDASI AKADEMIK (Future Directions & Novelty dari penalaran LLM)
    """
    profile = context.research_profile
    num_theses = len(context.theses) if context.theses else 0

    if not context.theses:
        # Kasus Bukti Tidak Cukup (Evidence Insufficient) -> Strict Abstention Report
        report = f"""# Research Gap Analysis

**Topik Analisis:** {context.query}

## 📌 Status Penelusuran Korpus Repositori IT Del
**Tidak ditemukan dokumen penelitian yang relevan dengan topik "{context.query}" dalam korpus repositori skripsi IT Del yang ditelusuri saat ini (Jumlah bukti relevan = 0).**

---

## ⚠️ Batasan Analisis (Evidence Abstention)
Karena tidak tersedianya bukti atau data penelitian terdahulu mengenai topik ini pada korpus repositori lokal yang terindeks, sistem **tidak dapat merumuskan research gap empiris lokal** ataupun menyimpulkan ketiadaan penelitian secara absolut di seluruh kampus IT Del.

---

## 🎯 Saran Arah Kajian Lanjutan
Untuk menyusun celah penelitian yang valid dan dapat dipertanggungjawabkan secara akademik pada topik ini, mahasiswa disarankan:
1. **Penelusuran Literatur Global:** Menelaah publikasi ilmiah internasional bereputasi (IEEE Xplore, ACM Digital Library, ScienceDirect) terkait {context.query}.
2. **Kajian Literatur Eksternal:** Mengidentifikasi batasan metodologi dan dataset dari publikasi global tersebut sebagai dasar perumusan usulan tugas akhir/skripsi baru."""
        context.analysis = report.strip()
        context.response = {
            "query": context.query,
            "ideas": report.strip(),
            "literature_review": report.strip(),
            "sources": [],
            "citations": [],
            "research_profile": profile.to_dict() if profile else {},
        }
        return context

    # 1. Bangun Evidence Matrix dari dokumen riil
    theses_str_list = []
    matrix_rows = []
    for idx, t in enumerate(context.theses, start=1):
        title = t.get('title', 'Untitled')
        author = t.get('author') or 'Unknown'
        year = t.get('year') or '-'
        prodi = t.get('prodi') or 'IT Del'
        abstract = t.get('abstract') or t.get('chunk') or ''
        
        # Gabungkan methodologies dan technologies agar metode/arsitektur (CNN, VGG-16, Xception, IoT) selalu terisi
        methods_list = t.get('methodologies', []) + t.get('technologies', [])
        clean_methods = [m.upper() if len(m) <= 4 else m.title() for m in dict.fromkeys(methods_list) if m]
        methods_str = ", ".join(clean_methods[:3]) if clean_methods else "Algoritma Terapan"

        # Gabungkan datasets dan domains agar objek/dataset selalu jelas
        datasets_list = t.get('datasets', []) + t.get('domains', [])
        clean_datasets = [d.title() for d in dict.fromkeys(datasets_list) if d]
        datasets_str = ", ".join(clean_datasets[:2]) if clean_datasets else "Data Primer / Lokal"

        # Rapikan judul (Title Case dan panjang optimal)
        clean_title = title.strip().title()
        if len(clean_title) > 60:
            clean_title = clean_title[:57] + "..."

        theses_str_list.append(
            f"[{idx}] Judul: {title}\n"
            f"    Penulis: {author} ({year}) | Prodi: {prodi}\n"
            f"    Metode Utama: {methods_str} | Dataset/Domain: {datasets_str}\n"
            f"    Kutipan/Abstrak: {abstract[:400]}"
        )
        matrix_rows.append(f"| [{idx}] | {clean_title} | {author} ({year}) | {methods_str} | {datasets_str} |")

    theses_str = "\n\n".join(theses_str_list)
    matrix_table_str = "\n".join(matrix_rows)

    prompt = f"""Anda adalah DELBot, Academic Intelligence System & Research Advisor Institut Teknologi Del.

==================================================
TOPIK ANALISIS RESEARCH GAP
==================================================
{context.query}

==================================================
DOKUMEN RUJUKAN RIIL DARI REPOSITORI IT DEL ({num_theses} Dokumen)
==================================================
{theses_str}

==================================================
PEDOMAN DISIPLIN BUKTI & INTEGRITAS AKADEMIK (STRICT ACADEMIC RESTRAINT):
==================================================
1. [FAKTA DOKUMEN]:
   - Seluruh nama peneliti, tahun, judul, metode, dan dataset rujukan HANYA boleh diambil dari Dokumen Rujukan di atas. DILARANG KERAS mengarang nama peneliti fiktif.
   - JANGAN mengklaim penelitian rujukan "membuktikan keberhasilan/akurasi tinggi" kecuali dokumen bukti secara eksplisit memuat angka metrik evaluasi. Cukup sebutkan bahwa metode tersebut telah diterapkan pada kasus yang tertera.

2. [INFERENSI PENELUSURAN - HINDARI KLAIM ABSOLUT]:
   - DILARANG menggunakan klaim absolut seperti "belum pernah diteliti di IT Del" atau "tidak pernah ada".
   - WAJIB gunakan formulasi yang tepat secara metodologis: "Dalam dokumen repositori IT Del yang berhasil ditemukan pada proses penelusuran saat ini, belum ditemukan penelitian yang secara spesifik membahas {context.query}."

3. [STATUS NOVELTY - NOVELTY OPPORTUNITY / CANDIDATE]:
   - Status kebaruan adalah KANDIDAT/PELUANG KEBARUAN (Novelty Opportunity), bukan kebaruan mutlak yang terkonfirmasi.
   - Formulasi wajib: "Dalam dokumen yang berhasil ditelusuri, belum ditemukan penerapan [metode] untuk [topik kueri]. Kondisi ini menunjukkan adanya peluang penelitian (novelty opportunity) yang dapat diajukan dan perlu divalidasi lebih lanjut melalui penelusuran literatur yang lebih luas."

4. [LABELING USULAN EKSPLORATIF]:
   - Beri label yang jelas bahwa rekomendasi arsitektur lanjutan (seperti ViT, Focal Loss, Grad-CAM++) dan dataset benchmark publik (seperti ISIC/HAM10000) merupakan "Rekomendasi eksploratif berbasis kajian keilmuan terkini, bukan temuan langsung dari dokumen repositori IT Del".

==================================================
FORMAT KELUARAN WAJIB (MARKDOWN AKADEMIK FORMAL):
==================================================
# Research Gap Analysis

**Topik Analisis:** {context.query}

## Matriks Bukti Penelitian Terdahulu (*Evidence Matrix*)
| Ref | Judul Skripsi Repositori IT Del | Penulis & Tahun | Metode Utama | Dataset / Kasus |
| :---: | :--- | :--- | :--- | :--- |
{matrix_table_str}

---

## Analisis Celah Riset Berbasis Bukti (*Evidence-Grounded Gap*)
* **Fakta Rujukan:** Penelitian [Nama Penulis 1] ([Tahun 1]) [1] dan [Nama Penulis 2] ([Tahun 2]) [2] menunjukkan bahwa metode [sebutkan metode dokumen] telah diterapkan pada pengolahan citra domain [sebutkan domain dokumen rujukan].
* **Celah Penelusuran Korpus:** Dalam dokumen repositori IT Del yang berhasil ditemukan pada proses penelusuran saat ini, penerapan arsitektur tersebut difokuskan pada [domain rujukan], sedangkan penelitian yang secara spesifik membahas **{context.query}** belum ditemukan.

---

## Peluang Penelitian Lanjutan (*Future Directions*)
*(Rekomendasi eksploratif berbasis metodologi terkini, bukan temuan langsung dari dokumen repositori IT Del)*
1. **Adaptasi Domain ke Citra Klinis:** Mengadaptasi arsitektur deep learning yang telah diterapkan pada skripsi rujukan menuju domain citra medis dengan penyesuaian prapemrosesan khusus (seperti normalisasi kontras dan reduksi artefak).
2. **Penanganan Ketimpangan Kelas (Class Imbalance):** Mengintegrasikan fungsi kerugian adaptif seperti *Focal Loss* atau *Class-Balanced Weighting* untuk menangani disparitas jumlah sampel antar-kelas lesi.
3. **Penerapan Interpretabilitas Model (Explainable AI):** Mengintegrasikan modul interpretabilitas seperti *Grad-CAM++* untuk memvisualisasikan fitur spasial yang mendasari inferensi model sebagai pendukung verifikasi klinis.

---

## Usulan Peluang Kebaruan (*Novelty Opportunity*)
* **Kajian Bukti Repositori:** Dokumen rujukan [1][2][3] menunjukkan penerapan metode [sebutkan metode] pada domain [sebutkan domain rujukan].
* **Status Celah Repositori:** Dalam dokumen yang berhasil ditelusuri, belum ditemukan penerapan metode tersebut untuk topik {context.query}. Kondisi ini menunjukkan adanya **peluang kebaruan (novelty opportunity)** yang potensial untuk dieksplorasi lebih lanjut.
* **Kandidat Usulan Kebaruan:** Mahasiswa dapat mengusulkan sistem klasifikasi {context.query} dengan integrasi arsitektur komparatif dan modul interpretabilitas (Grad-CAM++) sebagai usulan kontribusi yang terukur.

---

## Rekomendasi Dataset Acuan Publik
*(Panduan data terbuka untuk implementasi penelitian mandiri)*
* **Rekomendasi Dataset Acuan:** [Nama Dataset Publik Standar Domain Terkait, misal: ISIC Archive / HAM10000 Dataset / Kaggle Open Datasets] yang dapat diakses secara publik dan telah tervalidasi secara standar sebagai data acuan penelitian.
"""

    report = gateway.generate_response(prompt=prompt, max_tokens=2048)
    context.analysis = report.strip()
    context.response = {
        "query": context.query,
        "ideas": report.strip(),
        "literature_review": report.strip(),
        "sources": context.theses,
        "citations": context.citations,
        "research_profile": profile.to_dict() if profile else {},
    }
    return context
