#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.10
#
# Local Qdrant Mode Embedding Index
#
# MVP FALLBACK
#
# Purpose:
# Bypass unavailable Docker Qdrant
# Use local persistent Qdrant storage
#
# Input:
# pdf_chunk_manifest.json
#
# Output:
# embedding_index_result.json
#
# Tidak:
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

QDRANT_PATH="$ROOT/repository_data/qdrant_local"

OUTPUT="$ROOT/repository_data/mapping/embedding_index_result.json"


mkdir -p "$QDRANT_PATH"
mkdir -p "$(dirname "$OUTPUT")"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.10 Local Qdrant Mode Index"
echo "======================================================================"


python3 <<'PY'

import json
import os
from datetime import datetime


from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)


ROOT="/workspace/delbot"

chunk_file=f"{ROOT}/repository_data/mapping/pdf_chunk_manifest.json"

qdrant_path=f"{ROOT}/repository_data/qdrant_local"

output=f"{ROOT}/repository_data/mapping/embedding_index_result.json"


collection="delbot_mvp_documents"


with open(chunk_file,"r") as f:
    data=json.load(f)


chunks=data.get("chunks",[])


if len(chunks)==0:

    result={
        "status":"FAILED",
        "reason":"NO_CHUNKS_FOUND"
    }

    with open(output,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))

else:

    print("Chunks:",len(chunks))


    model_name="BAAI/bge-m3"

    print("Loading:",model_name)


    model=SentenceTransformer(
        model_name
    )


    client=QdrantClient(
        path=qdrant_path
    )


    existing=[
        c.name
        for c in client.get_collections().collections
    ]


    if collection not in existing:

        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=1024,
                distance=Distance.COSINE
            )
        )


    points=[]


    limit=min(
        len(chunks),
        5000
    )


    texts=[]


    for item in chunks[:limit]:

        if isinstance(item,dict):

            text=item.get(
                "text",
                ""
            )

        else:

            text=str(item)


        texts.append(text)


    vectors=model.encode(
        texts,
        batch_size=16,
        show_progress_bar=False
    )


    for idx,vector in enumerate(vectors):

        points.append(

            PointStruct(

                id=idx,

                vector=vector.tolist(),

                payload={
                    "text":texts[idx]
                }

            )

        )


    client.upsert(

        collection_name=collection,

        points=points

    )


    result={

        "timestamp":
            datetime.utcnow().isoformat()+"Z",

        "status":
            "SUCCESS",

        "mode":
            "LOCAL_QDRANT",

        "collection":
            collection,

        "indexed":
            len(points),

        "storage":
            qdrant_path

    }


    with open(output,"w") as f:

        json.dump(
            result,
            f,
            indent=2
        )


    print(
        json.dumps(
            result,
            indent=2
        )
    )


PY


echo
echo "======================================================================"
echo "Generated:"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.10 COMPLETE"

echo
echo "NEXT:"
echo "SUCCESS -> PR-5.7 Retrieval Engine"
echo "FAILED -> inspect chunk manifest"

echo
echo "Terminal tetap terbuka"

