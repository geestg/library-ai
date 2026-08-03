#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.9
#
# Repository Chat MVP
#
# SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# ==============================================================================

set -u

ROOT="/workspace/delbot"

DBDIR="$ROOT/repository_data/qdrant_local"

OUTDIR="$ROOT/repository_data/mapping"

OUTPUT="$OUTDIR/repository_chat.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.9 Repository Chat MVP"
echo "======================================================================"

python3 <<PY
import json
import pathlib
import traceback
from datetime import datetime

output=pathlib.Path(r"$OUTPUT")
dbdir=pathlib.Path(r"$DBDIR")

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":"QDRANT_LOCAL",
    "collection":"delbot_mvp_documents",
    "query":"Apa itu Computer Vision?",
    "answer":"",
    "context":[],
    "status":"FAILED"
}

try:

    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient

    model=SentenceTransformer("BAAI/bge-m3")

    client=QdrantClient(path=str(dbdir))

    collection="delbot_mvp_documents"

    vector=model.encode(
        result["query"],
        normalize_embeddings=True
    ).tolist()

    hits=client.search(
        collection_name=collection,
        query_vector=vector,
        limit=5
    )

    contexts=[]

    for h in hits:

        payload=h.payload or {}

        contexts.append({
            "document":payload.get("document"),
            "chunk_id":payload.get("chunk_id"),
            "score":round(float(h.score),4),
            "text":payload.get("text","")[:500]
        })

    answer=[]

    for i,c in enumerate(contexts,1):
        answer.append(
            f"[{i}] {c['text']}"
        )

    result["context"]=contexts

    result["answer"]="\n\n".join(answer)

    result["hits"]=len(contexts)

    result["status"]="SUCCESS"

except Exception:

    result["trace"]=traceback.format_exc()

output.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)

PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.10 LLM Answer Generator"
echo "FAILED  -> inspect repository_chat.json"

