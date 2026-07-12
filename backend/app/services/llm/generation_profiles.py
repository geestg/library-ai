class GenerationProfiles:

    # klasifikasi ya/tidak
    VERIFIER = {
        "temperature": 0,
        "max_tokens": 8,
    }

    # jawaban RAG normal
    ANSWER = {
        "temperature": 0,
    }

    # rewrite query
    QUERY_RESOLUTION = {
        "temperature": 0,
        "max_tokens": 32,
    }

    # judul chat
    TITLE = {
        "temperature": 0.3,
        "max_tokens": 32,
    }

    # literature review
    RESEARCH = {
        "temperature": 0.2,
    }

    # brainstorming
    CREATIVE = {
        "temperature": 0.7,
    }

