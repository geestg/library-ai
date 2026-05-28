from typing import List, Dict


def build_source_map(results: List[Dict]):

    """
    Build structured citation mapping
    from retrieval results.
    """

    citations = []

    for idx, result in enumerate(results, start=1):

        metadata = result.get("metadata", {})

        citation = {
            "source_id": idx,
            "source_file": metadata.get(
                "source_file",
                "Unknown"
            ),
            "page": metadata.get("page"),
            "chunk_index": metadata.get(
                "chunk_index"
            ),
            "score": result.get("score"),
            "content": result.get("text", "")
        }

        citations.append(citation)

    return citations