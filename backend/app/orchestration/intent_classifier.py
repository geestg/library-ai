def classify_intent(query: str):

    query = query.lower()

    # =====================================
    # FAQ
    # =====================================

    if any(word in query for word in [

        "halo",
        "hai",
        "siapa kamu",
        "help"
    ]):

        return "faq"

    # =====================================
    # MULTIMODAL
    # =====================================

    if any(word in query for word in [

        "gambar",
        "diagram",
        "pdf scan",
        "foto",
        "visual"
    ]):

        return "multimodal"

    # =====================================
    # RESEARCH GAP
    # =====================================

    if any(word in query for word in [

        "research gap",
        "gap penelitian",
        "novelty",
        "future work",
        "future research"
    ]):

        return "research_gap"

    # =====================================
    # TITLE GENERATION
    # =====================================

    if any(word in query for word in [

        "judul skripsi",
        "judul penelitian",
        "judul tugas akhir",
        "topik skripsi"
    ]):

        return "title_generation"

    # =====================================
    # LITERATURE REVIEW
    # =====================================

    if any(word in query for word in [

        "literature review",
        "related work",
        "state of the art",
        "penelitian sebelumnya"
    ]):

        return "literature"

    # =====================================
    # METHODOLOGY
    # =====================================

    if any(word in query for word in [

        "metodologi",
        "metode",
        "algoritma",
        "framework"
    ]):

        return "methodology"

    # =====================================
    # TECHNICAL
    # =====================================

    if any(word in query for word in [

        "cnn",
        "transformer",
        "bert",
        "embedding",
        "fine tuning",
        "vector database"
    ]):

        return "technical"

    # =====================================
    # DEFAULT
    # =====================================

    return "rag"