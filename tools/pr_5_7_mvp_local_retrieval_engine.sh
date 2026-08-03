#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.7
#
# Local Retrieval Engine (Qdrant Local)
#
# MVP SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

DBDIR="$ROOT/repository_data/qdrant_local"
MANIFEST="$ROOT/repository_data/mapping/pdf_chunk_manifest.json"

OUTDIR="$ROOT/repository_data/mapping"

OUTPUT="$OUTDIR/local_retrieval_engine.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.7 Local Retrieval Engine"
echo "======================================================================"

python3 <<PY
import json
import os

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

DB=r"$DBDIR"
MANIFEST=r"$MANIFEST"
OUTPUT=r"$OUTPUT"

COLLECTION="delbot_mvp_documents"

status="FAILED"
indexed=0
hits=0
query="computer vision"

client=None

try:

    client=QdrantClient(path=DB)

    cols=client.get_collections().collections

    names=[c.name for c in cols]

    if COLLECTION in names:

        info=client.get_collection(COLLECTION)

        indexed=info.points_count or 0

        model=SentenceTransformer(
            "BAAI/bge-m3",
            device="cpu"
        )

        vector=model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        result=client.search(
            collection_name=COLLECTION,
            query_vector=vector,
            limit=5
        )

        hits=len(result)

        status="SUCCESS"

except Exception as e:

    status="FAILED"
    error=str(e)

out={
    "backend":"QDRANT_LOCAL",
    "collection":COLLECTION,
    "indexed_points":indexed,
    "query":query,
    "top_k":5,
    "hits":hits,
    "status":status
}

if status!="SUCCESS":
    out["error"]=error

with open(OUTPUT,"w") as f:
    json.dump(out,f,indent=2)

print(json.dumps(out,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.8 Repository QA MVP"
echo "FAILED -> inspect local_retrieval_engine.json"

