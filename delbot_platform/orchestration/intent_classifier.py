import re

def classify_intent(query: str) -> str:
    q = query.lower()

    # =====================================
    # 1. LIBRARY / RECOMMENDATION
    # Harus DULUAN dicek agar "cari buku cnn" tidak jatuh ke technical
    # =====================================
    LIBRARY_TRIGGERS = [
        "cari buku", "cari referensi", "rekomendasi buku", "rekomendasikan buku",
        "saran buku", "referensi buku", "buku apa", "buku tentang",
        "buku yang membahas", "buku untuk", "bacaan apa", "bacaan untuk",
        "buku teks", "textbook", "lokasi buku", "lokasi rak", "di mana buku",
        "di mana rak", "di mana letak buku", "nomor klasifikasi", "rak buku",
        "lantai berapa", "koleksi buku", "perpustakaan", "library", "peminjaman",
        "meminjam buku", "jam buka", "jam perpustakaan", "batas buku", "denda buku",
        "find book", "search book", "recommend book", "book about", "books on",
        "books about", "book recommendation", "where is the book", "shelf location",
    ]
    if any(trigger in q for trigger in LIBRARY_TRIGGERS):
        return "recommendation"

    # =====================================
    # 2. FAQ (Word Boundary Matching agar "langchain" tidak match "hai")
    # =====================================
    FAQ_TRIGGERS = ["halo", "hai", "hi", "hey", "hello", "p", "siapa kamu", "help", "apa itu delbot", "kamu bisa apa", "selamat pagi", "selamat siang", "selamat sore", "selamat malam", "pagi", "siang", "sore", "malam"]
    for faq_word in FAQ_TRIGGERS:
        if re.search(r'\b' + re.escape(faq_word) + r'\b', q):
            return "faq"

    # =====================================
    # 3. MULTIMODAL
    # =====================================
    if any(word in q for word in ["gambar", "diagram", "pdf scan", "foto", "visual"]):
        return "multimodal"

    # =====================================
    # 4. NOVELTY / CORPUS CHECK (Apakah sudah ada skripsi X di IT Del?)
    # =====================================
    NOVELTY_CHECK_TRIGGERS = [
        "apakah sudah ada", "apakah pernah ada", "apakah ada skripsi",
        "sudah pernah diteliti", "apakah pernah dilakukan", "pernah diteliti",
        "pernah dilakukan sebelumnya", "apakah sudah pernah", "apakah ada penelitian",
        "cek kebaruan", "sudah ada skripsi", "apakah topik ini sudah"
    ]
    if any(trigger in q for trigger in NOVELTY_CHECK_TRIGGERS):
        return "novelty_check"

    # =====================================
    # 4b. RESEARCH GAP
    # =====================================
    if any(word in q for word in [
        "research gap", "gap penelitian", "novelty", "kebaruan penelitian",
        "future work", "future research", "celah penelitian", "celah riset"
    ]):
        return "research_gap"

    # =====================================
    # 5. METHODOLOGY & EXPLICIT PROCESS
    # Ditingkatkan agar "alur penelitian untuk skripsi" -> methodology
    # =====================================
    METHODOLOGY_EXPLICIT_TRIGGERS = [
        "metode penelitian", "metodologi", "framework penelitian",
        "alur penelitian", "tahapan penelitian", "langkah penelitian",
        "rancangan penelitian", "rancangan metodologi"
    ]
    if any(trigger in q for trigger in METHODOLOGY_EXPLICIT_TRIGGERS):
        return "methodology"

    # =====================================
    # 6. METHODOLOGY COMPARISON
    # =====================================
    if any(word in q for word in [
        "bandingkan", "perbandingan", "komparasi", "mana yang lebih baik",
        "perbedaan antara", "versus", " vs ", "compare", "comparison",
        "lebih baik antara", "mana yang cocok", "metode mana yang"
    ]):
        return "methodology_comparison"

    # =====================================
    # 7. TITLE GENERATION
    # =====================================
    TITLE_GEN_TRIGGERS = [
        "cari ide skripsi", "ide skripsi", "ide penelitian",
        "judul skripsi", "judul penelitian", "judul tugas akhir",
        "topik skripsi", "topik penelitian", "skripsi ai", "skripsi terkait",
        "mau skripsi", "mau buat skripsi", "cari topik skripsi",
        "bantu skripsi", "ide ta", "topik ta", "judul ta",
        "ide tugas akhir", "topik tugas akhir", "cari judul",
        "bantuan judul", "saran judul", "rekomendasikan judul",
        "rekomendasikan topik", "skripsi bidang", "skripsi tentang",
        "thesis idea", "thesis topic", "thesis title", "research idea",
        "research topic", "research title", "dissertation idea",
        "skripsi dong", "ta dong", "butuh ide skripsi", "minta ide skripsi"
    ]
    if any(trigger in q for trigger in TITLE_GEN_TRIGGERS):
        return "title_generation"

    # =====================================
    # 8. TOPIC EXPLORATION
    # =====================================
    if any(word in q for word in [
        "tren riset", "tren penelitian", "topik populer", "apa yang sedang populer",
        "hot topic", "emerging topic", "penelitian terkini", "riset terkini",
        "perkembangan terbaru", "teknologi terbaru di", "bidang apa yang menjanjikan"
    ]):
        return "topic_exploration"

    # =====================================
    # 9. LITERATURE REVIEW
    # =====================================
    if any(word in q for word in [
        "literature review", "tinjauan pustaka", "tinjauan literatur",
        "related work", "state of the art", "penelitian sebelumnya",
        "kajian literatur", "kajian pustaka"
    ]):
        return "literature"

    # =====================================
    # 10. TECHNICAL
    # =====================================
    TECHNICAL_TRIGGERS = [
        "cnn", "transformer", "bert", "lstm", "gru",
        "llm", "rag", "langchain", "fine tuning", "fine-tuning",
        "lora", "qlora", "prompt engineering", "chain of thought",
        "gemini", "chatgpt", "ollama", "embedding", "vector database",
        "vector store", "fastapi", "docker", "kubernetes", "yolo",
        "resnet", "efficientnet", "ocr", "esp32", "arduino", "mqtt",
        "raspberry pi"
    ]
    if any(word in q for word in TECHNICAL_TRIGGERS):
        return "technical"

    # =====================================
    # 11. DEFAULT FALLBACK
    # =====================================
    return "rag"