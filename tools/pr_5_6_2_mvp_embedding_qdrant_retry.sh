#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.2
#
# Embedding + Qdrant Retry Index
#
# MVP SAFE
# ==============================================================================
#
# Input:
# repository_data/mapping/pdf_chunk_manifest.json
#
# Output:
# repository_data/mapping/embedding_index_result.json
#
# Policy:
# PDF First
# Metadata Supplementary
#
# Tidak melakukan:
# - delete
# - migration
# - cleanup
# - restart service
#
# Terminal tetap terbuka
# ==============================================================================

set -u

ROOT="/workspace/delbot"

CHUNK_FILE="$ROOT/repository_data/mapping/pdf_chunk_manifest.json"

OUTPUT="$ROOT/repository_data/mapping/embedding_index_result.json"

COLLECTION="delbot_mvp_documents"

QDRANT_URL="http://localhost:6333"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.2 Embedding Qdrant Retry"
echo "======================================================================"


python3 <<'PY'

import json
import os
import sys
import time


ROOT="/workspace/delbot"

chunk_file=f"{ROOT}/repository_data/mapping/pdf_chunk_manifest.json"
output=f"{ROOT}/repository_data/mapping/embedding_index_result.json"

collection="delbot_mvp_documents"


result={
    "status":"FAILED",
    "collection":collection,
    "indexed":0,
    "message":""
}


# ==========================================================
# Check input
# ==========================================================

if not os.path.exists(chunk_file):

    result["message"]="chunk manifest missing"

else:

    try:

        from qdrant_client import QdrantClient
        from qdrant_client.models import VectorParams, Distance

        client=QdrantClient(
            url="http://localhost:6333",
            timeout=10
        )


        # health check

        collections=client.get_collections()


        with open(chunk_file,"r") as f:
            data=json.load(f)


        chunks=[]


        if isinstance(data,list):
            chunks=data

        elif isinstance(data,dict):

            for key in [
                "chunks",
                "documents",
                "items"
            ]:
                if key in data:
                    chunks=data[key]
                    break


        total=len(chunks)


        if total==0:

            result["message"]="no chunks detected"


        else:

            # MVP limit
            # avoid terminal/memory explosion

            chunks=chunks[:1000]


            from sentence_transformers import SentenceTransformer


            model=SentenceTransformer(
                "BAAI/bge-m3"
            )


            texts=[]

            for c in chunks:

                if isinstance(c,dict):

                    text=(
                        c.get("text")
                        or c.get("content")
                        or ""
                    )

                else:
                    text=str(c)


                texts.append(text[:2000])


            vectors=model.encode(
                texts,
                batch_size=32,
                show_progress_bar=False
            )


            vector_size=len(vectors[0])


            existing=[
                x.name
                for x in client.get_collections().collections
            ]


            if collection not in existing:

                client.create_collection(
                    collection_name=collection,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )


            points=[]

            for i,v in enumerate(vectors):

                payload={
                    "text":texts[i],
                    "source":"pdf_repository"
                }

                points.append(
                    {
                        "id":i,
                        "vector":v.tolist(),
                        "payload":payload
                    }
                )


            client.upsert(
                collection_name=collection,
                points=points
            )


            result["status"]="SUCCESS"
            result["indexed"]=len(points)
            result["message"]="embedding index completed"


    except Exception as e:

        result["message"]=str(e)[:300]



with open(output,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result,indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.6.2 COMPLETE"

echo

echo "NEXT"
echo "SUCCESS -> PR-5.7 Retrieval Engine"
echo "FAILED  -> inspect qdrant/model error"

echo

echo "Terminal remains open"

