import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')

from app.rag.thesis_bm25 import thesis_bm25_search

query = "optimasi klasifikasi citra medis deep learning"
print("--- TEST BM25 WITHOUT PRODI FILTER ---")
res1 = thesis_bm25_search(query, limit=5)
print(f"Count: {len(res1)}")
for idx, item in enumerate(res1[:3], 1):
    p = item.get("payload", {})
    print(f"  [{idx}] Title: {p.get('title')} | Prodi: {p.get('prodi')}")

print("\n--- TEST BM25 WITH prodi_names=['Informatika'] ---")
res2 = thesis_bm25_search(query, limit=5, prodi_names=["Informatika"])
print(f"Count: {len(res2)}")
for idx, item in enumerate(res2[:3], 1):
    p = item.get("payload", {})
    print(f"  [{idx}] Title: {p.get('title')} | Prodi: {p.get('prodi')}")
