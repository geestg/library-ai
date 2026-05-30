from typing import List, Dict


def build_source_map(
    results: List[Dict]
):
    """
    Build structured citation mapping
    from thesis retrieval results.
    """

    citations = []

    for idx, result in enumerate(
        results,
        start=1
    ):

        payload = result.get(
            "payload",
            {}
        )

        citation = {

            "source_id": idx,

            "title":
            payload.get(
                "title",
                ""
            ),

            "author":
            payload.get(
                "author",
                ""
            ),

            "year":
            payload.get(
                "year",
                ""
            ),

            "prodi":
            payload.get(
                "prodi",
                ""
            ),

            "url":
            payload.get(
                "url",
                ""
            ),

            "chunk_index":
            payload.get(
                "chunk_index"
            ),

            "score":
            result.get(
                "rerank_score",
                result.get(
                    "score",
                    0
                )
            ),

            "content":
            payload.get(
                "chunk",
                ""
            )
        }

        citations.append(
            citation
        )

    return citations