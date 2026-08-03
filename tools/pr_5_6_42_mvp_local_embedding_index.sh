#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.42
#
# Local Embedding Index
# (SentenceTransformers + Qdrant Local)
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

OUTDIR="$ROOT/repository_data/mapping"
DBDIR="$ROOT/repository_data/qdrant_local"

OUTPUT="$OUTDIR/local_embedding_index.json"

mkdir -p "$OUTDIR"
mkdir -p "$DBDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.42 Local Embedding Index"
echo "======================================================================"

python3 <<PY
import json
import traceback
from pathlib import Path

result={
    "backend":"QDRANT_LOCAL",
    "embedding_library":"SentenceTransformer",
    "embedding_model":"BAAI/bge-m3",
    "collection":"delbot_mvp_documents",
    "status":"FAILED"
}

try:

    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient

    model=SentenceTransformer("BAAI/bge-m3")

    client=QdrantClient(path="$DBDIR")

    result["sentence_transformers"]=True
    result["qdrant_local"]=True
    result["status"]="READY"

except Exception as e:

    result["error"]=str(e)
    result["trace"]=traceback.format_exc(limit=3)

Path("$OUTPUT").write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps(result,indent=2))

PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "READY -> PR-5.6.43"
echo "FAILED -> cek local_embedding_index.json"

