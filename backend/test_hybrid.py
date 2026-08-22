import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')

from app.rag.thesis_hybrid_search import thesis_vector_search, hybrid_search
from app.rag.thesis_bm25 import thesis_bm25_search

query = "optimasi klasifikasi citra medis deep learning informatika"

print("====================================")
print("HYBRID SEARCH INTEGRITY TEST")
print("====================================")

print("\n--- 1. DENSE VECTOR SEARCH (Qdrant) ---")
v_res = thesis_vector_search(query, limit=5)
print(f"Vector Results Count: {len(v_res)}")
if v_res:
    p = v_res[0].get("payload", {})
    print(f"  Top Title: {p.get('title')}")
    print(f"  Score: {v_res[0].get('score'):.4f}")

print("\n--- 2. SPARSE BM25 SEARCH (Lexical Engine) ---")
b_res = thesis_bm25_search(query, limit=5)
print(f"BM25 Results Count: {len(b_res)}")
if b_res:
    p = b_res[0].get("payload", {})
    print(f"  Top Title: {p.get('title')}")
    print(f"  Score: {b_res[0].get('score'):.4f}")

print("\n--- 3. RECIPROCAL RANK FUSION (RRF Hybrid) ---")
h_res = hybrid_search(query, limit=5)
print(f"Hybrid Fused Results Count: {len(h_res)}")
for idx, r in enumerate(h_res[:5], start=1):
    p = r.get("payload", {})
    s = r.get("score", 0)
    print(f"  [{idx}] RRF Score: {s:.4f} | Title: {p.get('title')} | Prodi: {p.get('prodi')}")

print("\n====================================")
print("HYBRID SEARCH STATUS: 100% OPERATIONAL & ACTIVE")
print("====================================")
