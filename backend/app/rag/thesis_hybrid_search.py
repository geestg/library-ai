from app.rag.hybrid_search import (
    hybrid_search as base_hybrid_search
)


# =====================================
# THESIS HYBRID SEARCH
# =====================================

def hybrid_search(
    query: str,
    limit: int = 20
):
    """
    Thesis dataset retrieval wrapper.

    Kept for backward compatibility
    with existing research service.
    """

    return base_hybrid_search(

        query=query,

        limit=limit
    )