from __future__ import annotations

import re
from qdrant_client.models import Filter, FieldCondition, MatchValue
from delbot_platform.research.retrieval.qdrant_client import client
from delbot_platform.core.constants import THESIS_DATASET_COLLECTION

GAP_KEYWORDS = [
    "saran", "selanjutnya", "mendatang", "diharapkan", "disarankan",
    "dapat dikembangkan", "keterbatasan", "kelemahan", "belum",
    "tidak mencakup", "dibatasi", "future work", "future studies",
    "pengembangan lebih lanjut", "penelitian berikutnya"
]

def extract_bab5_gaps(theses: list) -> list:
    """
    Ekstrak kalimat saran, keterbatasan, dan pengembangan lebih lanjut (Bab 5)
    dari skripsi relevan di Qdrant Vector Store.
    """
    gaps = []
    if not theses:
        return gaps
        
    target_titles = {t.get("title", "").lower().strip() for t in theses if t.get("title")}
    if not target_titles:
        return gaps
        
    try:
        response = client.scroll(
            collection_name=THESIS_DATASET_COLLECTION,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="source_bab", match=MatchValue(value="bab5"))
                ]
            ),
            limit=5000,
            with_payload=True,
            with_vectors=False
        )
        points = response[0]
        
        for point in points:
            payload = point.payload or {}
            title = payload.get("title", "")
            if title.lower().strip() not in target_titles:
                continue
                
            chunk_text = payload.get("chunk", payload.get("text", ""))
            if not chunk_text:
                continue
                
            sentences = re.split(r'(?<=[.!?])\s+', chunk_text)
            for sentence in sentences:
                sentence_clean = sentence.strip()
                if not sentence_clean or len(sentence_clean) < 20 or len(sentence_clean) > 300:
                    continue
                    
                sentence_lower = sentence_clean.lower()
                matched = any(kw in sentence_lower for kw in GAP_KEYWORDS)
                if matched:
                    gaps.append({
                        "title": title,
                        "author": payload.get("author", payload.get("penulis", "Unknown")),
                        "year": payload.get("year", payload.get("tahun", "-")),
                        "prodi": payload.get("prodi", "-"),
                        "sentence": sentence_clean
                    })
    except Exception as e:
        print(f"[BAB 5 EXTRACTOR QDRANT ERROR] {e}")
            
    return gaps
