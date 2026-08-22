import re

THESIS_IDEA_KEYWORDS = [
    "ide skripsi",
    "judul skripsi",
    "thesis idea",
    "research idea",
    "topik skripsi",
    "proposal skripsi",
    "novelty",
    "rekomendasi ide",
    "rekomendasi judul",
    "mencari ide",
    "meneliti",
    "tertarik tentang",
    "tertarik meneliti",
    "penelitian tentang"
]

LITERATURE_REVIEW_KEYWORDS = [
    "literature review",
    "tinjauan pustaka",
    "state of the art",
    "penelitian terdahulu",
    "kajian pustaka",
    "bab 2",
    "sistematika",
    "review paper",
    "ringkasan penelitian"
]

PRODI_ALIASES = {
    "trpl": [
        "teknologi rekayasa perangkat lunak",
        "trpl",
        "d4 trpl",
        "rekayasa perangkat lunak",
        "rpl",
        "software engineering",
    ],
    "sistem_informasi": [
        "sistem informasi",
        "si",
        "prodi si",
        "information system",
        "sisfo",
    ],
    "informatika": [
        "informatika",
        "if",
        "ilmu komputer",
        "computer science",
        "teknik informatika",
        "informaika",
    ],
    "teknologi_informasi": [
        "teknologi informasi",
        "ti",
        "prodi ti",
        "information technology",
    ],
    "teknologi_komputer": [
        "teknologi komputer",
        "tk",
        "computer technology",
        "d3 tk",
    ],
    "teknik_elektro": [
        "teknik elektro",
        "te",
        "electrical engineering",
        "elektro",
        "elktro",
    ],
    "manajemen_rekayasa": [
        "manajemen rekayasa",
        "mr",
        "engineering management",
        "rekayasa manajemen",
    ],
    "teknik_metalurgi": [
        "teknik metalurgi",
        "tm",
        "metallurgical engineering",
        "metalurgi",
        "metalurg",
    ],
    "teknologi_bioproses": [
        "teknologi bioproses",
        "teknik bioproses",
        "tb",
        "bioprocess engineering",
        "bioproses",
        "bioprosess",
        "teknik bioprosess",
        "bio proses",
        "bioprocess",
    ],
    "bioteknologi": [
        "bioteknologi",
        "biotek",
        "biotechnology",
    ],
}


def normalize_research_query(query: str) -> str:
    q = (query or "").lower()
    replacements = {
        "generate ide judul skripsi": "",
        "generate ide skripsi": "",
        "ide judul skripsi": "",
        "judul skripsi": "",
        "ide skripsi": "",
        "research idea": "",
        "thesis idea": "",
        "generate": ""
    }
    for old, new in replacements.items():
        q = q.replace(old, new)
    return q.strip()


def is_thesis_idea_query(query: str) -> bool:
    query_lc = (query or "").lower()
    if any(keyword in query_lc for keyword in THESIS_IDEA_KEYWORDS):
        return True

    patterns = [
        r"\b(ide|judul|topik|penelitian)\b",
        r"\b(buatkan|rekomendasi|cari|butuh)\b.*\b(skripsi|tugas akhir)\b",
        r"\btertarik\b.*\b(meneliti|riset)\b",
        r"\b(mau|ingin|berencana)\b.*\b(meneliti|riset)\b",
        r"\b(saya|aku)\b.*\b(tertarik|ingin)\b.*\b(penelitian|meneliti)\b",
    ]
    for pattern in patterns:
        if re.search(pattern, query_lc):
            return True

    try:
        import numpy as np
        from app.services.embedder.embedding_gateway import embedding_gateway

        intent_examples = [
            "Saya ingin mendapatkan ide skripsi untuk topik penelitian.",
            "Tolong buatkan judul dan ide penelitian tugas akhir.",
            "Saya tertarik meneliti sebuah topik dan butuh rekomendasi penelitian.",
            "Ide untuk skripsi tentang pengembangan sistem atau metode penelitian.",
            "Rekomendasi ide penelitian untuk tesis atau skripsi.",
        ]

        def _cosine_sim(a, b):
            a = np.array(a, dtype=float)
            b = np.array(b, dtype=float)
            denom = (np.linalg.norm(a) * np.linalg.norm(b))
            if denom == 0:
                return 0.0
            return float(np.dot(a, b) / denom)

        q_emb = embedding_gateway.embed(query_lc)
        sims = []
        for ex in intent_examples:
            ex_emb = embedding_gateway.embed(ex)
            sims.append(_cosine_sim(q_emb, ex_emb))

        if sims and max(sims) >= 0.75:
            return True
    except Exception as e:
        print(f"[INTENT_DETECTOR] semantic fallback failed: {e}")

    return False


def is_literature_review_query(query: str) -> bool:
    query_lc = (query or "").lower()
    if any(keyword in query_lc for keyword in LITERATURE_REVIEW_KEYWORDS):
        return True

    patterns = [
        r"\b(tinjauan|review|kajian)\b.*\b(pustaka|literature|artikel|jurnal)\b",
        r"\b(state of the art|sota)\b",
        r"\b(cari|buat|susun|tuliskan)\b.*\b(literature review|tinjauan pustaka)\b",
        r"\b(penelitian terdahulu|kajian pustaka)\b",
    ]
    for pattern in patterns:
        if re.search(pattern, query_lc):
            return True

    try:
        import numpy as np
        from app.services.embedder.embedding_gateway import embedding_gateway

        intent_examples = [
            "Saya ingin membuat literature review atau tinjauan pustaka.",
            "Tolong susun kajian pustaka dan penelitian terdahulu untuk topik saya.",
            "Saya butuh state of the art dan ringkasan penelitian pada bidang tertentu.",
            "Cari artikel jurnal untuk literature review tentang topik penelitian.",
            "Saya ingin menulis bab kajian pustaka dari penelitian sebelumnya.",
        ]

        def _cosine_sim(a, b):
            a = np.array(a, dtype=float)
            b = np.array(b, dtype=float)
            denom = (np.linalg.norm(a) * np.linalg.norm(b))
            if denom == 0:
                return 0.0
            return float(np.dot(a, b) / denom)

        q_emb = embedding_gateway.embed(query_lc)
        sims = []
        for ex in intent_examples:
            ex_emb = embedding_gateway.embed(ex)
            sims.append(_cosine_sim(q_emb, ex_emb))

        if sims and max(sims) >= 0.75:
            return True
    except Exception as e:
        print(f"[INTENT_DETECTOR] semantic fallback failed: {e}")

    return False


def detect_prodi_from_query(query: str) -> str:
    query_lc = (query or "").lower()

    # Kata-kata dan entitas yang TIDAK BOLEH dianggap nama prodi eksternal
    NON_PRODI_BLACKLIST = {
        "ide", "di", "atas", "sebelumnya", "tersebut", "ini", "itu", "jawaban",
        "penjelasan", "pilihan", "opsi", "rekomendasi", "metode", "algoritma",
        "model", "deep", "learning", "machine", "saran", "hasil", "tabel",
        "beberapa", "semua", "banyak", "antara", "salah", "satu", "contoh",
        "berbagai", "daftar", "point", "poin", "nomor", "no", "perspektif",
        "it", "del", "it_del", "institut", "teknologi", "kampus", "universitas",
        "mahasiswa", "skripsi", "tugas", "akhir", "ta", "penelitian"
    }

    # 1. TAHAP 1: DETEKSI POLA EKSPLISIT (HIGH CONFIDENCE)
    # Mencari pola 'saya [prodi]', 'prodi [prodi]', 'dari [prodi]', 'jurusan [prodi]', 'terkait [prodi]'
    explicit_patterns = [
        r'\b(?:prodi|saya|dari|jurusan|mahasiswa|anak|angkatan|terkait|seputar|bidang|mengenai)\s+([a-z0-9\s]+)',
    ]

    for pattern in explicit_patterns:
        matches = re.findall(pattern, query_lc)
        for val in matches:
            val_clean = val.strip()
            # Potong kata-kata sambung/kata kerja yang mengikuti nama prodi
            val_clean_prodi = re.split(r'\b(?:mau|butuh|ingin|tentang|cari|skripsi|tugas|akhir|yang|untuk|dengan|berbasis|ada|bisa|tolong)\b', val_clean)[0].strip()

            # Jika frasa mengandung IT Del / Del / Institut Teknologi Del, abaikan (bukan nama prodi eksternal)
            if any(del_kw in val_clean_prodi.lower() for del_kw in ["it del", "it_del", "institut teknologi del", "kampus del"]):
                # Cek apakah setelah membuang IT Del masih ada nama prodi (misal: "informatika it del")
                val_clean_prodi = re.sub(r'\b(?:it\s*del|it_del|institut\s*teknologi\s*del|kampus\s*del|del)\b', '', val_clean_prodi, flags=re.IGNORECASE).strip()
                if not val_clean_prodi:
                    continue

            # Cek apakah value setelah kata pengenal cocok dengan prodi manapun di IT Del
            for prodi_slug, aliases in PRODI_ALIASES.items():
                for alias in aliases:
                    if len(alias) <= 2:
                        if re.search(r'\b' + re.escape(alias) + r'\b', val_clean_prodi):
                            print(f"[PRODI_DETECTOR] Explicit match found via pattern: '{prodi_slug}' (value: '{val_clean_prodi}')")
                            return prodi_slug
                    else:
                        if alias in val_clean_prodi:
                            print(f"[PRODI_DETECTOR] Explicit match found via pattern: '{prodi_slug}' (value: '{val_clean_prodi}')")
                            return prodi_slug

            # Abaikan frasa rujukan percakapan umum yang bukan prodi
            val_clean_lower = val_clean_prodi.lower()
            if any(phrase in val_clean_lower for phrase in [
                "ide di atas", "pertanyaan di atas", "jawaban di atas", "pilihan di atas",
                "opsi di atas", "hasil di atas", "tabel di atas", "dari ide", "dari 5 ide",
                "sebelumnya", "di atas", "it del", "del"
            ]):
                continue

            # Cek kata per kata setelah dibersihkan dari tanda baca
            clean_prodi_str = re.sub(r'^(?:mahasiswa|anak|prodi|jurusan)\s+', '', val_clean_prodi, flags=re.IGNORECASE).strip()
            words = [w.strip(".,;:?!'\"()[]") for w in clean_prodi_str.split() if w.strip(".,;:?!'\"()[]")]

            # Abaikan jika mengandung kata-kata blacklist
            if any(w.lower() in NON_PRODI_BLACKLIST for w in words):
                continue

            if words and len(words) <= 4:
                non_del_prodi = " ".join(words)
                if non_del_prodi.lower() not in ["it del", "del", "it_del", "itdel"]:
                    print(f"[PRODI_DETECTOR] Explicit non-DEL prodi detected: '{non_del_prodi}'")
                    return f"bukan_del:{non_del_prodi}"

    # 2. TAHAP 2: FALLBACK ALIAS BIASA (LOW CONFIDENCE)
    # Jika tidak ada pola eksplisit, cari prodi yang disebut paling belakang 
    # (biasanya deklarasi prodi ditaruh di akhir kalimat) atau urutkan kecocokan alias terpanjang.
    matched_prodis = []
    
    for prodi_slug, aliases in PRODI_ALIASES.items():
        for alias in aliases:
            if len(alias) <= 2:
                pattern = r'\b' + re.escape(alias) + r'\b'
                match = re.search(pattern, query_lc)
                if match:
                    matched_prodis.append((prodi_slug, match.start(), len(alias)))
            else:
                if alias in query_lc:
                    idx = query_lc.find(alias)
                    matched_prodis.append((prodi_slug, idx, len(alias)))
                    
    if matched_prodis:
        # Urutkan berdasarkan panjang alias (yang lebih spesifik dulu)
        # Jika panjang sama, urutkan berdasarkan letaknya di kueri (yang paling akhir)
        matched_prodis.sort(key=lambda x: (x[2], x[1]), reverse=True)
        # Jika ada deklarasi diri (seperti 'saya' atau 'dari' elektro), utamakan prodi itu
        for prodi, idx, length in matched_prodis:
            # Cek apakah ada kata kunci penjelas dekat indeks kecocokan
            context_area = query_lc[max(0, idx-15):idx]
            if any(self_word in context_area for self_word in ["saya", "prodi", "dari", "jurusan"]):
                print(f"[PRODI_DETECTOR] Context-aware fallback match: '{prodi}'")
                return prodi
        
        # Default: ambil prodi dengan alias terpanjang/terakhir
        selected_prodi = matched_prodis[0][0]
        print(f"[PRODI_DETECTOR] Fallback match: '{selected_prodi}'")
        return selected_prodi
        
    return ""
