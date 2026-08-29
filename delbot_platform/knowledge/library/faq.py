from __future__ import annotations

import re

# =========================================
# FAQ DATA — PERPUSTAKAAN DEL
# =========================================

FAQ_LIST = [
    {
        "keywords": ["halo", "hai", "hi", "hey", "hello", "p", "selamat pagi", "selamat siang", "selamat sore", "selamat malam", "pagi", "siang", "sore", "malam"],
        "answer": (
            "Halo! 👋 Saya DELBot, asisten cerdas Perpustakaan dan Riset IT Del. "
            "Ada yang bisa saya bantu terkait pencarian buku, referensi akademik, atau ide penelitian skripsi Anda hari ini?"
        ),
    },
    {
        "keywords": ["terima kasih", "terimakasih", "makasih", "thank you", "thanks", "ok", "oke", "siap", "nuhun", "suwun"],
        "answer": (
            "Sama-sama! Senang bisa membantu Anda. Jika ada hal lain yang Anda butuhkan di kemudian hari, "
            "jangan ragu untuk bertanya lagi. Selamat belajar dan semoga sukses!"
        ),
    },
    {
        "keywords": ["siapa kamu", "siapa anda", "kamu itu apa", "apa itu delbot", "perkenalkan", "delbot library"],
        "answer": (
            "Saya adalah DELBot, AI Assistant Perpustakaan Institut Teknologi Del. "
            "Saya siap membantu Anda mencari buku, memberikan rekomendasi bacaan, "
            "dan menjawab pertanyaan seputar koleksi perpustakaan."
        ),
    },
    {
        "keywords": [
            "jam buka", "jam operasional", "jam berapa", "buka jam", "tutup jam", "waktu buka",
            "jam tutup", "kapan buka", "kapan tutup", "hari apa saja buka", "sabtu buka", "minggu buka", "hari libur",
            "sekarang buka", "sekarang tutup", "buka sekarang", "buka perpus", "tutup perpus", "apakah buka", "buka tidak",
            "buka ga", "buka nggak", "hari ini buka", "besok buka", "hari buka", "senin buka", "selasa buka", "rabu buka", "kamis buka", "jumat buka"
        ],
        "answer": (
            "Jam Operasional Perpustakaan IT Del:\n"
            "• Senin – Jumat: 08.00 – 21.45 WIB\n"
            "• Sabtu: 08.00 – 12.00 WIB\n"
            "• Minggu & Hari Libur Nasional: Tutup"
        ),
    },
    {
        "keywords": [
            "cara pinjam", "pinjam buku", "meminjam", "prosedur pinjam", "peminjaman", "pinjam",
            "cara meminjam", "syarat pinjam", "prosedur peminjaman", "maksimal buku", "berapa buku",
            "maksimal pinjam", "berapa lama", "durasi pinjam", "batas pinjam", "aturan pinjam",
            "aturan peminjaman", "kuota pinjam", "jumlah buku yang boleh dipinjam"
        ],
        "answer": (
            "Aturan Peminjaman Buku Perpustakaan IT Del:\n"
            "• Batas Maksimal Peminjaman: 3 buku untuk mahasiswa.\n"
            "• Durasi Peminjaman: Maksimal 1 minggu (7 hari).\n"
            "• Prosedur: Pilih buku di rak sesuai nomor klasifikasi, lalu serahkan ke petugas sirkulasi dengan menunjukkan Kartu Mahasiswa (KTM)."
        ),
    },
    {
        "keywords": ["denda", "terlambat", "telat kembalikan", "biaya denda", "sanksi", "bayar denda", "denda per hari", "denda terlambat"],
        "answer": (
            "Jika terlambat mengembalikan buku, denda adalah Rp2.000 per hari per buku."
        ),
    },
    {
        "keywords": ["lokasi perpustakaan", "dimana perpustakaan", "letak perpustakaan", "gedung perpustakaan", "di mana perpustakaan", "dimana perpus", "lokasi rak", "letak rak", "klasifikasi buku"],
        "answer": (
            "Perpustakaan IT Del berlokasi di Gedung Utama. Tata letak lokasi buku di rak berdasarkan nomor klasifikasi:\n"
            "• Klasifikasi 001 – 600: Lantai 1\n"
            "• Klasifikasi 600an – 999: Lantai 2\n"
            "• Koleksi Lainnya: Lantai 2 Gedung Baru"
        ),
    },
    {
        "keywords": ["lokasi kampus", "dimana kampus", "alamat kampus", "dimana it del", "lokasi it del", "dimana del", "alamat it del", "posisi kampus", "alamat del", "dimana lokasi kampus"],
        "answer": (
            "Institut Teknologi Del (IT Del) berlokasi di:\n"
            "📍 Jl. Sisingamangaraja, Sitoluama, Kecamatan Laguboti, Kabupaten Toba, Sumatera Utara, Kode Pos 22381.\n\n"
            "Kampus IT Del terletak indah di tepi Danau Toba!"
        ),
    },
    {
        "keywords": ["pendiri del", "pendiri it del", "siapa pendiri", "siapa yang mendirikan", "siapa yang membangun", "siapa pembuat del", "siapa yang buat", "yayasan del", "luhut", "luhut binsar", "sejarah del"],
        "answer": (
            "Institut Teknologi Del (IT Del) didirikan oleh Jenderal TNI (Purn.) Luhut Binsar Pandjaitan "
            "bersama istrinya, Ibu Devi Pandjaitan (Simatupang), di bawah naungan Yayasan Del pada tahun 2001. "
            "Kampus IT Del berdiri indah di Laguboti, Kabupaten Toba, Sumatera Utara."
        ),
    },
    {
        "keywords": ["tata tertib", "aturan perpus", "peraturan perpustakaan", "makan minum", "bawa makanan", "bawa minuman", "pakai jaket", "sweater", "topi", "titip tas", "loker"],
        "answer": (
            "Tata tertib masuk Perpustakaan IT Del:\n"
            "1. Tidak membawa makanan atau minuman.\n"
            "2. Tidak menggunakan jaket, sweater, dan topi.\n"
            "3. Menitipkan tas, pouch, dan botol minum di loker.\n"
            "4. Hanya buku catatan yang diperbolehkan dibawa masuk."
        ),
    },
    {
        "keywords": ["hak kewajiban", "kewajiban perpus", "tanggung jawab", "kehilangan", "barang hilang", "berduaan", "lawan jenis"],
        "answer": (
            "Hak & Kewajiban Pengguna Perpustakaan IT Del:\n"
            "1. Mengisi log pengunjung yang telah disediakan.\n"
            "2. Menjaga ketenangan dan kebersihan.\n"
            "3. Menggunakan fasilitas dengan tertib dan bijak.\n"
            "4. Menghindari berduaan dengan lawan jenis.\n\n"
            "Himbauan: Mohon tidak meninggalkan barang pribadi. Segala bentuk kehilangan barang bukan merupakan tanggung jawab pihak perpustakaan."
        ),
    },
    {
        "keywords": ["apa yang bisa", "bisa apa", "fitur", "kemampuan", "help", "bantuan", "bisa bantu apa", "fitur delbot", "cara pakai"],
        "answer": (
            "Saya bisa membantu Anda:\n"
            "• 📚 Mencari buku berdasarkan judul, penulis, atau topik\n"
            "• 🎯 Merekomendasikan buku sesuai kebutuhan Anda\n"
            "• 📍 Memberikan informasi lokasi rak buku\n"
            "• ℹ️ Menjawab pertanyaan seputar perpustakaan\n\n"
            "Contoh: 'Rekomendasikan buku machine learning untuk pemula'"
        ),
    },
    {
        "keywords": ["berapa buku", "jumlah koleksi", "total buku", "koleksi berapa", "berapa banyak buku", "jumlah buku", "koleksi buku"],
        "answer": (
            "Perpustakaan IT Del saat ini memiliki **8.206 judul buku** terdaftar di katalog digital "
            "yang mencakup berbagai bidang ilmu komputer, teknik, dan sains."
        ),
    },
    {
        "keywords": ["kembalikan buku", "cara kembalikan", "pengembalian", "kembali buku", "cara mengembalikan", "pengembalian buku"],
        "answer": (
            "Untuk mengembalikan buku:\n"
            "1. Bawa buku ke meja petugas perpustakaan\n"
            "2. Serahkan buku beserta kartu peminjaman\n"
            "3. Petugas akan memproses pengembalian\n"
            "4. Pastikan buku dikembalikan sebelum tanggal jatuh tempo"
        ),
    },
    {
        "keywords": ["kalender akademik", "jadwal akademik", "tahun akademik 2026", "kegiatan akademik", "kapan kuliah", "kapan masuk", "hari pertama kuliah", "libur natal", "libur tahun baru", "libur idul fitri"],
        "answer": (
            "Ringkasan Kalender Akademik IT Del T.A. 2026/2027:\n"
            "• Hari Pertama Kuliah Gasal: 7 September 2026\n"
            "• Hari Pertama Kuliah Genap: 15 Februari 2027\n"
            "• Libur Natal & Tahun Baru: 21 Desember 2026 – 5 Januari 2027\n"
            "• Libur Idul Fitri: 9 Maret – 11 Maret 2027"
        ),
    },
    {
        "keywords": ["krs", "prs", "kapan krs", "kapan prs", "perwalian", "pengisian krs", "perubahan rencana studi"],
        "answer": (
            "Jadwal Perwalian, KRS & PRS T.A. 2026/2027:\n"
            "• **Semester Gasal**:\n"
            "  - Perwalian & Pengisian KRS: 31 Agustus – 4 September 2026\n"
            "  - Perubahan Rencana Studi (PRS): 14 – 20 September 2026\n"
            "• **Semester Genap**:\n"
            "  - Perwalian & Pengisian KRS: 8 – 12 Februari 2027\n"
            "  - Perubahan Rencana Studi (PRS): 22 – 28 Februari 2027"
        ),
    },
    {
        "keywords": ["uts", "uas", "ujian tengah semester", "ujian akhir semester", "kapan uts", "kapan uas"],
        "answer": (
            "Jadwal Ujian (UTS & UAS) T.A. 2026/2027:\n"
            "• **Semester Gasal**:\n"
            "  - Ujian Tengah Semester (UTS): 26 – 30 Oktober 2026\n"
            "  - Ujian Akhir Semester (UAS): 11 – 15 Januari 2027\n"
            "• **Semester Genap**:\n"
            "  - Ujian Tengah Semester (UTS): 12 – 16 April 2027\n"
            "  - Ujian Akhir Semester (UAS): 7 – 11 Juni 2027"
        ),
    },
    {
        "keywords": ["wisuda", "dies natalis", "dies natalis 25", "dies natalis it del", "kapan wisuda", "wisuda 2026", "Dies Natalis IT Del ke-25"],
        "answer": (
            "Jadwal Wisuda & Dies Natalis IT Del Tahun 2026:\n"
            "• Batas Akhir Pendaftaran Wisuda: 20 Agustus 2026\n"
            "• Pelaksanaan Wisuda 2026: 25 September 2026\n"
            "• Pengukuhan Mahasiswa Baru & Dies Natalis ke-25: 26 September 2026"
        ),
    },
    {
        "keywords": ["mahasiswa baru", "maba", "asrama", "kapan masuk asrama", "masuk asrama", "angkatan 26", "angkatan 27", "pkkmb", "pca", "matrikulasi", "gasing"],
        "answer": (
            "Jadwal Kegiatan Mahasiswa Baru IT Del:\n"
            "• **Angkatan XXVI (T.A. 2026/2027)**:\n"
            "  - Masuk Asrama: 15 Agustus 2026\n"
            "  - Kegiatan PCA (Program Cinta Almamater): 16 – 20 Agustus 2026\n"
            "  - Matrikulasi: 21 – 26 Agustus 2026\n"
            "  - Kegiatan Gasing: 27 Agustus – 2 September 2026\n"
            "• **Angkatan XXVII (T.A. 2027/2028)**:\n"
            "  - Pendaftaran Maba: 2 November 2026 – 6 Agustus 2027\n"
            "  - Masuk Asrama: 16 Agustus 2027"
        ),
    },
    {
        "keywords": ["kerja praktik", "kp", "penjajakan kp", "pembekalan kp", "kapan kp", "kerja praktek"],
        "answer": (
            "Jadwal Pelaksanaan Kerja Praktik (KP) T.A. 2026/2027:\n"
            "• Masa Penjajakan Tempat KP: 9 Februari – 11 Juni 2027\n"
            "• Batas Akhir Penentuan Tempat KP: 11 Juni 2027\n"
            "• Pembekalan KP: 4 Juni 2027\n"
            "• Pelaksanaan KP di Perusahaan: 14 Juni – 4 September 2027"
        ),
    },
]

# =========================================
# HELPER: CLEAN & TOKENIZE
# =========================================

def _get_tokens(text: str) -> set[str]:
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return set(cleaned.split())

# =========================================
# FAQ SCORER & MATCHER
# =========================================

def calculate_match_score(query: str, query_tokens: set[str], keyword: str) -> float:
    """
    Menghitung tingkat kecocokan kueri dengan kata kunci FAQ secara fleksibel.
    """
    keyword_clean = keyword.lower().strip()
    keyword_tokens = _get_tokens(keyword_clean)
    
    if not keyword_tokens:
        return 0.0

    # 1. Exact Phrase Match (Prioritas Tertinggi) dengan batas kata (word boundaries)
    escaped_kw = re.escape(keyword_clean).replace(r"\ ", r"\s+")
    pattern = re.compile(rf"\b{escaped_kw}\b", re.IGNORECASE)
    if pattern.search(query):
        return 5.0

    # 2. Irisan Kata (Intersection)
    intersection = query_tokens.intersection(keyword_tokens)
    overlap_ratio = len(intersection) / len(keyword_tokens)

    if overlap_ratio == 1.0:
        return 3.0
    elif overlap_ratio >= 0.7:
        return 1.5

    return 0.0

def answer_faq(query: str) -> str | None:
    """
    Cocokkan query secara cerdas dengan FAQ list menggunakan logika token overlap.
    """
    query_clean = query.lower().strip()

    # Bypass FAQ jika kueri menanyakan spesifik anggota (misal: 'apakah tiffani...') atau analitik sirkulasi (misal: 'paling sering dipinjam')
    dynamic_triggers = [
        "paling sering", "paling banyak", "terbanyak", "terpopuler", "sering dipinjam",
        "banyak dipinjam", "paling populer", "buku terpopuler", "populer",
        "pernah", "apakah", "siapa", "siapa yang", "siapa saja", "daftar peminjam",
        "riwayat", "statistik", "analisis", "tren"
    ]
    if any(trig in query_clean for trig in dynamic_triggers):
        return None

    query_tokens = _get_tokens(query_clean)


    best_match = None
    best_score = 0.0

    for faq in FAQ_LIST:
        item_best_score = 0.0
        for kw in faq["keywords"]:
            score = calculate_match_score(query_clean, query_tokens, kw)
            if score > item_best_score:
                item_best_score = score
                
        if item_best_score > best_score:
            best_score = item_best_score
            best_match = faq

    if best_match and best_score >= 1.5:
        print(f"[FAQ SERVICE] Matched intent FAQ with score {best_score} for keywords {best_match['keywords']}")
        return best_match["answer"]

    return None
