from app.services.llm.model_gateway import gateway
from app.services.research.models.research_models import ResearchContext


def generate_method_comparison(context: ResearchContext) -> ResearchContext:
    """
    Generator Laporan Analisis & Komparasi Metodologi Riset.
    Menangani kueri perbandingan metode seperti:
    "Bandingkan penggunaan YOLO dan SSD pada skripsi mahasiswa IT Del"
    """
    profile = context.research_profile
    theses = context.theses or []

    # 1. KASUS A: DOKUMEN REPOSITORI TERSEDIA (Theses >= 1)
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
                f"    Metode: {methods}\n"
                f"    Ringkasan Hasil/Evaluasi: {abstract[:400]}"
            )
        theses_str = "\n\n".join(theses_str_list)

        prompt = f"""Anda adalah DELBot, Academic Intelligence System & Research Advisor Institut Teknologi Del.

==================================================
PERMINTAAN KOMPARASI METODOLOGI
==================================================
"{context.query}"

==================================================
DOKUMEN RUJUKAN SKRIPSI IT DEL ({len(theses)} Dokumen):
==================================================
{theses_str}

==================================================
TUGAS UTAMA:
==================================================
1. Bandingkan metode yang ditanyakan berdasarkan bukti empiris dari dokumen skripsi IT Del di atas.
2. Buat tabel perbandingan komparatif (Metode, Kelebihan, Keterbatasan, Penggunaan di IT Del) dengan sitasi `[1]`, `[2]`.
3. DILARANG KERAS menghasilkan daftar 5 ide skripsi baru! Fokus murni pada analisis perbandingan metode.

==================================================
FORMAT KELUARAN WAJIB (MARKDOWN):
==================================================
# Analisis Komparasi Metodologi Penelitian

**Topik Analisis:** {context.query}

## 📊 Tabel Perbandingan Empiris Berdasarkan Repositori IT Del
| Aspek Evaluasi | Metode A | Metode B | Rujukan Skripsi IT Del |
| :--- | :--- | :--- | :--- |
| **Arsitektur Utama** | ... | ... | [1] |
| **Kinerja / Akurasi** | ... | ... | [1], [2] |
| **Kelebihan** | ... | ... | [1] |
| **Keterbatasan** | ... | ... | [2] |

---

## 🔍 Pembahasan Komparasi Metodologi
* [Uraikan perbandingan secara mendalam berbasis rujukan bukti]

---

## 💡 Rekomendasi Pemilihan Metode
* [Rekomendasi kondisi penggunaan metode yang paling tepat untuk skripsi lanjutan]
"""
        response_text = gateway.generate_response(prompt=prompt, max_tokens=1000)
    else:
        # 2. KASUS B: TIDAK DITEMUKAN BUKTI SPESIFIK DI KORPUS IT DEL (Theses == 0)
        prompt = f"""Anda adalah DELBot, Academic Intelligence System & Research Advisor Institut Teknologi Del.

==================================================
PERMINTAAN KOMPARASI METODOLOGI
==================================================
"{context.query}"

==================================================
STATUS PENELUSURAN KORPUS:
==================================================
Tidak ditemukan skripsi mahasiswa IT Del yang secara spesifik membandingkan metode tersebut dalam korpus repositori yang ditelusuri (Jumlah dokumen = 0).

==================================================
TUGAS UTAMA:
==================================================
1. Sampaikan secara eksplisit di awal bahwa **tidak ditemukan bukti/skripsi perbandingan metode tersebut dalam korpus repositori IT Del yang ditelusuri**.
2. Berikan analisis perbandingan teoretis & standar industri internasional (SOTA) untuk menjawab kebutuhan pengguna secara ilmiah dan objektif.
3. Buat tabel perbandingan teoretis (Karakteristik Arsitektur, Kecepatan/Latency, Akurasi/mAP, Kebutuhan Komputasi, Kasus Penggunaan Ideal).
4. DILARANG KERAS menghasilkan daftar 5 ide skripsi baru! Fokus murni pada perbandingan metode.

==================================================
FORMAT KELUARAN WAJIB (MARKDOWN):
==================================================
# Analisis Komparasi Metodologi Penelitian

**Topik Analisis:** {context.query}

## 📌 Status Penelusuran Repositori IT Del
**Tidak ditemukan skripsi mahasiswa IT Del yang secara spesifik membandingkan kedua metode tersebut dalam korpus yang ditelusuri saat ini.** Oleh karena itu, sistem tidak dapat menyimpulkan data kinerja empiris lokal mahasiswa IT Del untuk perbandingan ini.

---

## 📊 Perbandingan Teoretis & Benchmark Standar
Berikut adalah analisis perbandingan komparatif berdasarkan literatur ilmiah standar:

| Parameter Komparasi | Metode 1 | Metode 2 |
| :--- | :--- | :--- |
| **Karakteristik Arsitektur** | ... | ... |
| **Kecepatan Inferensi** | ... | ... |
| **Akurasi / Deteksi Objek** | ... | ... |
| **Kebutuhan Komputasi** | ... | ... |
| **Kasus Penggunaan Ideal** | ... | ... |

---

## 🔍 Pembahasan Kelebihan & Keterbatasan
* **Kelebihan & Batasan Metode 1:** ...
* **Kelebihan & Batasan Metode 2:** ...

---

## 💡 Rekomendasi Pemilihan Metode untuk Tugas Akhir / Skripsi
* [Panduan pemilihan metode berdasarkan ketersediaan hardware dan kebutuhan akurasi vs kecepatan]
"""
        response_text = gateway.generate_response(prompt=prompt, max_tokens=1000)

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
