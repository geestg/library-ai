#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.40
#
# Local Embedding Index (Qdrant Local)
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

MANIFEST="$ROOT/repository_data/mapping/pdf_chunk_manifest.json"
OUTDIR="$ROOT/repository_data/mapping"
LOCALDB="$ROOT/repository_data/qdrant_local"

RESULT="$OUTDIR/local_embedding_index.json"

mkdir -p "$OUTDIR"
mkdir -p "$LOCALDB"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.40 Local Embedding Index"
echo "======================================================================"

python3 <<'PY'
import json
import os
import traceback

ROOT="/workspace/delbot"

manifest=os.path.join(ROOT,"repository_data/mapping/pdf_chunk_manifest.json")
local_db=os.path.join(ROOT,"repository_data/qdrant_local")
result_file=os.path.join(ROOT,"repository_data/mapping/local_embedding_index.json")

result={
    "backend":"QDRANT_LOCAL",
    "collection":"delbot_mvp_documents",
    "indexed":0,
    "status":"FAILED"
}

try:

    if not os.path.exists(manifest):
        result["status"]="MANIFEST_NOT_FOUND"

    else:

        with open(manifest,"r",encoding="utf-8") as f:
            data=json.load(f)

        chunks=[]

        if isinstance(data,list):
            chunks=data

        elif isinstance(data,dict):

            if isinstance(data.get("chunks"),list):
                chunks=data["chunks"]

            elif isinstance(data.get("documents"),list):
                chunks=data["documents"]

            elif isinstance(data.get("items"),list):
                chunks=data["items"]

        from FlagEmbedding import BGEM3FlagModel
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance
        from qdrant_client.models import VectorParams
        from qdrant_client.models import PointStruct

        model=BGEM3FlagModel(
            "BAAI/bge-m3",
            use_fp16=False
        )

        client=QdrantClient(path=local_db)

        names=[
            c.name
            for c in client.get_collections().collections
        ]

        if "delbot_mvp_documents" not in names:

            client.create_collection(
                collection_name="delbot_mvp_documents",
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE
                )
            )

        batch=[]
        indexed=0

        for idx,item in enumerate(chunks):

            if indexed>=5000:
                break

            text=""

            if isinstance(item,dict):
                text=item.get("text","")

            if not text.strip():
                continue

            emb=model.encode(
                [text]
            )["dense_vecs"][0]

            payload=item if isinstance(item,dict) else {"text":text}

            batch.append(
                PointStruct(
                    id=indexed+1,
                    vector=emb,
                    payload=payload
                )
            )

            indexed+=1

            if len(batch)>=64:

                client.upsert(
                    collection_name="delbot_mvp_documents",
                    points=batch
                )

                batch=[]

        if batch:

            client.upsert(
                collection_name="delbot_mvp_documents",
                points=batch
            )

        result["indexed"]=indexed
        result["status"]="SUCCESS"

except Exception as e:

    result["status"]="FAILED"
    result["error"]=str(e)
    result["trace"]=traceback.format_exc(limit=2)

with open(result_file,"w",encoding="utf-8") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))

PY

echo
echo "======================================================================"
echo "Generated"
echo "$RESULT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.7 Retrieval Engine MVP"
echo "FAILED  -> inspect local_embedding_index.json"

