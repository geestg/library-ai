from __future__ import annotations

import re
from typing import List, Callable, Optional

# =========================================
# INTENT KEYWORDS Constants
# =========================================

FAQ_KEYWORDS = [
    # Greetings & Closings
    "halo", "hai", "hello", "selamat pagi", "selamat siang", "selamat sore", "assalamualaikum", "hi", "hey",
    "terima kasih", "terimakasih", "makasih", "thank you", "thanks", "nuhun", "suwun",
    # Identity, Names & Help
    "nama saya", "namaku", "nama ku", "panggil saya", "panggil aku", "kenalkan", "kenalan", "apa kabar", "apakabar", "bagaimana kabar", "halo delbot", "hi delbot",
    "siapa kamu", "siapa anda", "kamu itu apa", "apa itu delbot", "perkenalkan", "delbot library",
    "bisa bantu apa", "fitur delbot", "cara pakai", "help", "bantuan", "apa yang bisa", "bisa apa",
    # Operational Hours
    "jam buka", "jam tutup", "jam operasional", "jam berapa", "buka jam", "tutup jam", "waktu buka",
    "kapan buka", "kapan tutup", "hari apa saja buka", "sabtu buka", "minggu buka", "hari libur",
    # Fines
    "denda", "terlambat", "telat kembalikan", "biaya denda", "sanksi", "bayar denda", "denda per hari", "denda terlambat",
    # Borrowing & Returning
    "cara pinjam", "pinjam buku", "meminjam", "prosedur pinjam", "peminjaman", "pinjam", "cara meminjam", "syarat pinjam", "prosedur peminjaman",
    "kembalikan buku", "cara kembalikan", "pengembalian", "kembali buku", "cara mengembalikan", "pengembalian buku",
    # Library Location & Building
    "lokasi perpustakaan", "dimana perpustakaan", "letak perpustakaan", "gedung perpustakaan", "di mana perpustakaan", "dimana perpus",
    # Stats
    "berapa buku", "jumlah koleksi", "total buku", "koleksi berapa", "berapa banyak buku", "jumlah buku", "koleksi buku",
    # Campus Info & Website Web Search Keywords
    "rektor", "pimpinan", "ketua del", "sejarah del", "pendiri del", "visi del", "misi del",
    "prodi", "program studi", "jurusan", "fakultas", "fite", "fti", "vokasi",
    "pmb", "pendaftaran del", "masuk del", "beasiswa del", "fasilitas del", "asrama del",
    "tentang del", "institut teknologi del", "it del", "kampus del", "siapa rektor",
    "ukt", "biaya", "spp", "bpp", "uang pangkal", "biaya kuliah", "biaya ukt"
]

STATUS_KEYWORDS = [
    "lokasi buku", "lokasi rak", "rak",
    "di lantai", "di rak", "letak buku", "posisi buku", "nomor klasifikasi",
]

METADATA_KEYWORDS = [
    "karangan", "karya", "ditulis oleh", "penulis",
    "penerbit", "tahun terbit", "edisi",
    "isbn", "klasifikasi",
]

RECOMMENDATION_KEYWORDS = [
    "rekomendasikan", "rekomendasi", "saran buku", "sarankan",
    "buku apa", "buku yang bagus", "referensi buku",
    "bacaan apa", "buku terkait", "buku tentang",
    "buku untuk belajar", "buku pemula", "buku mahir",
    "mau belajar", "ingin belajar", "cari buku",
    "carikan buku", "butuh buku",
]


def contains_keyword(text: str, keywords: List[str]) -> bool:
    """
    Mengecek apakah kata kunci ada di dalam teks dengan aman (menghindari substring collision).
    """
    words = set(re.findall(r"\b\w+\b", text.lower()))
    for kw in keywords:
        kw_clean = kw.lower().strip()
        if " " in kw_clean:
            if kw_clean in text:
                return True
        else:
            if kw_clean in words:
                return True
    return False


def route_intent(query: str, faq_checker: Optional[Callable[[str], Optional[str]]] = None) -> str:
    """
    Menentukan intent kueri secara cerdas menggunakan keyword matching dan FAQ service.
    Memiliki hierarki prioritas yang ketat agar pencarian buku tidak tertelan ke FAQ.
    """
    normalized_query = query.lower().strip()

    if len(normalized_query) < 3 and not normalized_query.isdigit():
        return "faq"

    # 1. Aturan Khusus Jam Operasional & Kalender Akademik (Pasti FAQ)
    if any(w in normalized_query for w in ["buka", "tutup", "jadwal", "operasional", "kapan"]):
        if any(w in normalized_query for w in ["perpus", "perpustakaan", "sekarang", "hari ini", "besok", "kapan", "jam", "hari", "krs", "uts", "uas", "wisuda", "pca", "matrikulasi", "libur"]):
            return "faq"

    # 2. Aturan Khusus Regulasi Peminjaman / Denda / SOP (Pasti FAQ)
    borrow_rules_triggers = [
        "lama masa peminjaman", "masa pinjam", "lama pinjam", "batas waktu pinjam",
        "denda", "biaya denda", "denda keterlambatan", "denda per hari",
        "syarat meminjam", "syarat pinjam", "cara pinjam", "prosedur pinjam",
        "maksimal buku yang bisa dipinjam", "jumlah maksimal buku yang bisa dipinjam", "berapa buku yang bisa dipinjam"
    ]
    if any(br in normalized_query for br in borrow_rules_triggers):
        return "faq"

    # 3. PRIORITAS UTAMA: Lokasi Rak Fisik Buku
    if contains_keyword(normalized_query, STATUS_KEYWORDS) or any(w in normalized_query for w in ["lokasi rak", "di rak", "letak buku", "posisi buku", "rak lantai"]):
        return "status"

    # 4. PRIORITAS UTAMA: Metadata Pengarang, Penerbit, Karya Buku
    if contains_keyword(normalized_query, METADATA_KEYWORDS) or any(w in normalized_query for w in ["karangan", "karya", "ditulis oleh", "penerbit", "buku terbitan", "pengarang"]):
        return "metadata"

    # 5. PRIORITAS UTAMA: Rekomendasi & Pencarian Katalog Buku
    book_triggers = [
        "cari buku", "carikan buku", "rekomendasi buku", "rekomendasikan buku",
        "buku tentang", "buku apa", "ada buku", "referensi buku", "daftar buku",
        "buku pemrograman", "buku fisika", "buku matematika", "buku algoritma",
        "buku jaringan", "buku sistem", "buku iot", "buku manajemen", "buku untuk"
    ]
    if contains_keyword(normalized_query, RECOMMENDATION_KEYWORDS) or any(bt in normalized_query for bt in book_triggers):
        return "recommendation"

    # 6. Pengecekan FAQ Institusi & Knowledge Base Statis
    if (faq_checker and faq_checker(query) is not None) or contains_keyword(normalized_query, FAQ_KEYWORDS):
        return "faq"

    # 7. Fallback kata pemicu buku umum jika tersisa
    generic_book_triggers = ["buku", "katalog", "bacaan", "referensi", "isbn"]
    if any(w in normalized_query for w in generic_book_triggers):
        return "recommendation"

    # 8. Default untuk pertanyaan umum natural language: rute ke "faq"
    return "faq"
