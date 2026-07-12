def normalize_research_query(
    query: str
):

    q = query.lower()

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

        q = q.replace(
            old,
            new
        )

    return q.strip()

