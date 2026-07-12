from typing import Literal


DocumentType = Literal[
    "research_paper",
    "thesis",
    "guidebook",
    "proposal",
    "report",
    "book",
    "presentation",
    "assignment",
    "cv",
    "general"
]


# =====================================
# HELPERS
# =====================================

def contains_any(
    content: str,
    keywords: list[str]
) -> bool:

    return any(

        keyword in content

        for keyword in keywords

    )


# =====================================
# DOCUMENT CLASSIFIER
# =====================================

def classify_document(
    text: str
) -> str:

    if not text:

        return "general"

    content = text.lower()

    content = content[:50000]

    # =================================
    # GUIDEBOOK
    # =================================

    guidebook_keywords = [

        "guidebook",
        "competition guidebook",
        "technical meeting",
        "final round",
        "preliminary round",
        "timeline",
        "timeline dan ketentuan",
        "ketentuan peserta",
        "narahubung",
        "registrasi",
        "pendaftaran",
        "hackathon",
        "perlombaan",
        "kompetisi",
        "submission",
        "pengumuman finalis",
        "presentasi dan demo produk"

    ]

    if contains_any(
        content,
        guidebook_keywords
    ):

        return "guidebook"

    # =================================
    # THESIS / SKRIPSI
    # =================================

    thesis_keywords = [

        "skripsi",
        "tesis",
        "disertasi",
        "program studi",
        "fakultas",
        "bab i",
        "bab ii",
        "bab iii",
        "bab iv",
        "bab v",
        "rumusan masalah",
        "tujuan penelitian",
        "manfaat penelitian",
        "metode penelitian"

    ]

    if contains_any(
        content,
        thesis_keywords
    ):

        return "thesis"

    # =================================
    # RESEARCH PAPER
    # =================================

    research_keywords = [

        "abstract",
        "keywords",
        "introduction",
        "related work",
        "literature review",
        "methodology",
        "results",
        "discussion",
        "conclusion",
        "references",
        "experimental setup"

    ]

    score = sum(

        1

        for keyword in research_keywords

        if keyword in content

    )

    if score >= 3:

        return "research_paper"

    # =================================
    # PROPOSAL
    # =================================

    proposal_keywords = [

        "latar belakang",
        "tujuan",
        "anggaran",
        "rencana kegiatan",
        "jadwal kegiatan",
        "proposal kegiatan",
        "proposal penelitian",
        "rancangan solusi",
        "estimasi biaya"

    ]

    proposal_score = sum(

        1

        for keyword in proposal_keywords

        if keyword in content

    )

    if proposal_score >= 3:

        return "proposal"

    # =================================
    # PRESENTATION
    # =================================

    presentation_keywords = [

        "agenda",
        "thank you",
        "questions",
        "slide",
        "overview",
        "presentation",
        "pitch deck"

    ]

    if contains_any(
        content,
        presentation_keywords
    ):

        return "presentation"

    # =================================
    # REPORT
    # =================================

    report_keywords = [

        "laporan",
        "hasil kegiatan",
        "evaluasi kegiatan",
        "kesimpulan kegiatan",
        "ringkasan kegiatan",
        "laporan akhir",
        "laporan pelaksanaan"

    ]

    if contains_any(
        content,
        report_keywords
    ):

        return "report"

    # =================================
    # CV
    # =================================

    cv_keywords = [

        "curriculum vitae",
        "riwayat hidup",
        "education",
        "work experience",
        "skills",
        "experience",
        "certification"

    ]

    if contains_any(
        content,
        cv_keywords
    ):

        return "cv"

    # =================================
    # BOOK
    # =================================

    book_keywords = [

        "chapter 1",
        "chapter 2",
        "chapter 3",
        "isbn",
        "copyright",
        "publisher",
        "table of contents"

    ]

    if contains_any(
        content,
        book_keywords
    ):

        return "book"

    # =================================
    # ASSIGNMENT
    # =================================

    assignment_keywords = [

        "tugas",
        "assignment",
        "instruksi pengerjaan",
        "petunjuk pengerjaan",
        "jawablah pertanyaan",
        "soal nomor",
        "penilaian"

    ]

    if contains_any(
        content,
        assignment_keywords
    ):

        return "assignment"

    # =================================
    # DEFAULT
    # =================================

    return "general"

