#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.43
#
# Local Embedding Build (SentenceTransformers + Qdrant Local)
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

CHUNK_MANIFEST="$ROOT/repository_data/mapping/pdf_chunk_manifest.json"
OUTDIR="$ROOT/repository_data/mapping"
OUTPUT="$OUTDIR/local_embedding_build.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.43 Local Embedding Build"
echo "======================================================================"

python3 <<PY
import json
import traceback
from pathlib import Path

result={
    "backend":"sentence_transformers",
    "model":"BAAI/bge-m3",
    "collection":"delbot_mvp_documents",
    "chunks":0,
    "embedded":0,
    "status":"FAILED"
}

try:

    manifest=Path("$CHUNK_MANIFEST")

    if not manifest.exists():
        raise FileNotFoundError(str(manifest))

    data=json.loads(manifest.read_text())

    chunks=[]

    if isinstance(data,list):
        chunks=data

    elif isinstance(data,dict):

        if isinstance(data.get("chunks"),list):
            chunks=data["chunks"]

        elif isinstance(data.get("documents"),list):
            for doc in data["documents"]:
                if isinstance(doc,dict):
                    chunks.extend(doc.get("chunks",[]))

    result["chunks"]=len(chunks)

    from sentence_transformers import SentenceTransformer

    model=SentenceTransformer("BAAI/bge-m3")

    sample=[]

    for c in chunks[:100]:

        if isinstance(c,str):
            sample.append(c)

        elif isinstance(c,dict):

            text=(
                c.get("text")
                or c.get("content")
                or c.get("chunk")
                or ""
            )

            if text.strip():
                sample.append(text)

    if sample:

        emb=model.encode(
            sample,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        result["embedded"]=len(emb)

    result["status"]="SUCCESS"

except Exception as e:

    result["error"]=str(e)
    result["trace"]=traceback.format_exc(limit=2)

Path("$OUTPUT").write_text(
    json.dumps(result,indent=2)
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
echo "SUCCESS -> PR-5.6.44 Local Qdrant Index"
echo "FAILED  -> inspect local_embedding_build.json"

