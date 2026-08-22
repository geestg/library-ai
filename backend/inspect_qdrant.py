import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')

from app.rag.qdrant_client import client
from app.core.constants import THESIS_DATASET_COLLECTION

points, _ = client.scroll(
    collection_name=THESIS_DATASET_COLLECTION,
    limit=20,
    with_payload=True,
    with_vectors=False
)

print(f"Total points fetched for sample: {len(points)}")
prodi_values = set()
for p in points:
    payload = p.payload or {}
    prodi_values.add(payload.get("prodi"))
    print(f"ID: {p.id} | Title: {payload.get('title')[:40]}... | Prodi: {payload.get('prodi')!r}")

print("\nAll Unique 'prodi' values in Qdrant payload sample:")
print(prodi_values)
