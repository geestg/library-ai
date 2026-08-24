from __future__ import annotations

from typing import List, Optional, Dict
from rank_bm25 import BM25Okapi
from delbot_platform.core.constants import LIBRARY_BOOKS_COLLECTION
from delbot_platform.research.retrieval.qdrant_client import client

_bm25_index: Optional[BM25Okapi] = None
_bm25_documents: List[str] = []
_bm25_payloads: List[dict] = []


def normalize_result(payload: dict, score: float) -> dict:
    return {
        "payload": payload,
        "score": score,
        "title": payload.get("title", ""),
        "author": payload.get("author", payload.get("penulis", "")),
        "subject": payload.get("subject", payload.get("subjek", "")),
        "publisher": payload.get("publisher", payload.get("penerbit", "")),
        "description": payload.get("description", payload.get("deskripsi", "")),
        "isbn": payload.get("isbn", ""),
        "location": payload.get("location", payload.get("lokasi", "")),
        "year": payload.get("published_at", payload.get("year", "")),
        "published_at": payload.get("published_at", ""),
        "classification_number": payload.get("classification_number", ""),
    }


def initialize_bm25():
    global _bm25_index, _bm25_documents, _bm25_payloads

    _bm25_documents = []
    _bm25_payloads = []

    # 1. Coba ambil dari Qdrant
    try:
        response = client.scroll(
            collection_name=LIBRARY_BOOKS_COLLECTION,
            limit=10000,
            with_payload=True,
            with_vectors=False,
        )

        points = response[0]
        for point in points:
            payload = point.payload or {}
            title = payload.get("title", "")
            subject = payload.get("subject", payload.get("subjek", ""))
            author = payload.get("author", payload.get("penulis", ""))
            description = payload.get("description", payload.get("deskripsi", ""))
            publisher = payload.get("publisher", payload.get("penerbit", ""))

            text = f"{title} {subject} {author} {description} {publisher}"

            if not text.strip():
                continue

            _bm25_documents.append(text)
            _bm25_payloads.append(payload)

    except Exception as qdrant_err:
        print(f"[LIBRARY BM25] Qdrant scroll unavailable ({qdrant_err}). Falling back to local library.db.")

    # 2. Fallback ke database lokal SQLite library.db (8.206 buku IT Del)
    if not _bm25_documents:
        import sqlite3
        import os
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workflows/dataset/library.db"))
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("SELECT id, title, author, publisher, published_year, subject, classification_number, location, isbn FROM books;")
                rows = cur.fetchall()
                for r in rows:
                    payload = {
                        "id": r[0],
                        "title": r[1] or "",
                        "author": r[2] or "",
                        "publisher": r[3] or "",
                        "year": str(r[4]) if r[4] else "",
                        "published_at": str(r[4]) if r[4] else "",
                        "subject": r[5] or "",
                        "classification_number": r[6] or "",
                        "location": r[7] or "",
                        "isbn": r[8] or "",
                        "description": r[5] or ""
                    }
                    text = f"{payload['title']} {payload['subject']} {payload['author']} {payload['publisher']}"
                    if text.strip():
                        _bm25_documents.append(text)
                        _bm25_payloads.append(payload)
                conn.close()
                print(f"[LIBRARY BM25] Loaded {len(_bm25_documents)} catalog books from local library.db.")
            except Exception as db_err:
                print(f"[LIBRARY BM25] SQLite fallback error: {db_err}")

    if _bm25_documents:
        tokenized = [doc.lower().split() for doc in _bm25_documents]
        _bm25_index = BM25Okapi(tokenized)
        print(f"[LIBRARY BM25] Initialized with {len(_bm25_documents)} books")
    else:
        _bm25_index = None
        print("[LIBRARY BM25] No books found in collection or local database")


def bm25_search(query: str, limit: int = 50) -> List[dict]:
    global _bm25_index

    if _bm25_index is None:
        initialize_bm25()

    if _bm25_index is None:
        return []

    tokenized_query = query.lower().strip().split()
    scores = _bm25_index.get_scores(tokenized_query)

    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    results = []
    for idx, score in ranked[:limit]:
        if score <= 0:
            continue
        results.append(
            normalize_result(_bm25_payloads[idx], float(score))
        )
    return results
