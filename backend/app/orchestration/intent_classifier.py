def classify_intent(query: str):

    query = query.lower()

    if any(word in query for word in [
        "halo",
        "hai",
        "siapa kamu",
        "help"
    ]):
        return "faq"

    if any(word in query for word in [
        "gambar",
        "diagram",
        "pdf scan",
        "foto",
        "visual"
    ]):
        return "multimodal"

    if any(word in query for word in [
        "analisis",
        "research gap",
        "metodologi",
        "judul skripsi"
    ]):
        return "reasoning"

    return "rag"