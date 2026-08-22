import sys
sys.path.insert(0, r'd:\DEL\library-ai\backend')

from app.rag.qdrant_client import client

cols = client.get_collections()
print("SUCCESS! Connected to Qdrant!")
print("Active Collections:", [c.name for c in cols.collections])
