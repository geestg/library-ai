from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import numpy as np

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def retrieve_relevant_chunks(

    pages,

    query: str,

    top_k: int = 8

):

    chunks = []

    for page in pages:

        page_num = page.get(
            "page",
            0
        )

        text = page.get(
            "text",
            ""
        )

        paragraphs = [

            p.strip()

            for p in text.split("\n\n")

            if p.strip()
        ]

        for paragraph in paragraphs:

            chunks.append({

                "page":
                page_num,

                "text":
                paragraph

            })

    if not chunks:

        return []

    texts = [

        c["text"]

        for c in chunks
    ]

    chunk_vectors = model.encode(

        texts,

        normalize_embeddings=True

    )

    query_vector = model.encode(

        query,

        normalize_embeddings=True

    )

    scores = cosine_similarity(

        [query_vector],

        chunk_vectors

    )[0]

    ranked_idx = np.argsort(
        scores
    )[::-1]

    results = []

    for idx in ranked_idx[:top_k]:

        results.append({

            "score":
            float(scores[idx]),

            "page":
            chunks[idx]["page"],

            "text":
            chunks[idx]["text"]

        })

    return results
