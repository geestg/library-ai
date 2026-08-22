from __future__ import annotations

import re

NOISE_PATTERNS = [
    r"(?i)^di\s+mana\s+lokasi\s+rak\s+untuk\s+buku\s+",
    r"(?i)^di\s+mana\s+lokasi\s+rak\s+buku\s+",
    r"(?i)^di\s+mana\s+lokasi\s+buku\s+",
    r"(?i)^lokasi\s+rak\s+buku\s+",
    r"(?i)^cari\s+buku\s+tentang\s+",
    r"(?i)^buku\s+tentang\s+",
    r"(?i)^rekomendasi\s+buku\s+",
    r"(?i)^buku\s+apa\s+yang\s+",
    r"(?i)^bisa\s+carikan\s+buku\s+",
]

BILINGUAL_TERMS = {
    "struktur data": "data structures",
    "algoritma": "algorithms",
    "sistem operasi": "operating systems",
    "jaringan komputer": "computer networking",
    "basis data": "database systems",
    "kecerdasan buatan": "artificial intelligence",
    "pembelajaran mesin": "machine learning",
    "pembelajaran mendalam": "deep learning",
    "rekayasa perangkat lunak": "software engineering",
    "pemrograman web": "web programming",
    "pemrograman terstruktur": "structured programming",
    "pemrograman berorientasi objek": "object oriented programming",
    "keamanan siber": "cybersecurity",
    "keamanan jaringan": "network security",
    "sistem tertanam": "embedded systems",
    "pengolahan citra": "image processing",
    "visi komputer": "computer vision",
    "pemrosesan bahasa alami": "natural language processing",
    "analisis data": "data analytics",
    "sains data": "data science",
    "penambangan data": "data mining",
    "sistem pakar": "expert systems",
    "interaksi manusia komputer": "human computer interaction",
    "komputasi awan": "cloud computing",
    "sistem terdistribusi": "distributed systems",
    "sistem informasi manajemen": "management information systems",
}


def clean_search_query(query: str) -> str:
    """
    Membersihkan noise percakapan umum dari kueri pencarian buku.
    """
    clean_query = query.strip()
    for pattern in NOISE_PATTERNS:
        clean_query = re.sub(pattern, "", clean_query)
    return clean_query.strip(" ?!.")


def expand_bilingual_terms(clean_query: str) -> str:
    """
    Mengekspansi istilah kueri Bahasa Indonesia ke Bahasa Inggris untuk Cross-Encoder & BM25 matching.
    """
    expanded_terms = []
    clean_lower = clean_query.lower()
    for id_term, en_term in BILINGUAL_TERMS.items():
        if id_term in clean_lower and en_term not in clean_lower:
            expanded_terms.append(en_term)

    if expanded_terms:
        return ' '.join(expanded_terms)
    return clean_query
