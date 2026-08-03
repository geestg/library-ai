#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6
#
# Embedding Pipeline + Qdrant Index MVP
#
# MVP SAFE
# ==============================================================================
#
# Input:
# - repository_data/mapping/pdf_chunk_manifest.json
#
# Output:
# - Qdrant collection
#   delbot_mvp_documents
#
# Policy:
# PDF First
# Metadata Supplementary
#
# Tidak melakukan:
# - delete collection
# - migration
# - cleanup
# - restart service
# - exit
#

set -u


ROOT="/workspace/delbot"

CHUNK_FILE="$ROOT/repository_data/mapping/pdf_chunk_manifest.json"

COLLECTION="delbot_mvp_documents"

EMBED_MODEL="BAAI/bge-m3"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6 Embedding Pipeline + Qdrant Index"
echo "======================================================================"


python3 <<'PY'

import os
import json
import uuid
from datetime import datetime


ROOT="/workspace/delbot"

chunk_file = (
    ROOT +
    "/repository_data/mapping/pdf_chunk_manifest.json"
)


collection = "delbot_mvp_documents"


if not os.path.exists(chunk_file):

    print(json.dumps({
        "status": "FAILED",
        "reason": "chunk_manifest_missing"
    }, indent=2))

else:

    with open(chunk_file) as f:
        data=json.load(f)


    chunks=[]


    if isinstance(data, dict):

        if "chunks" in data:
            chunks=data["chunks"]

        elif "documents" in data:

            for doc in data["documents"]:
                if "chunks" in doc:
                    chunks.extend(
                        doc["chunks"]
                    )


    print(
        "Detected chunks:",
        len(chunks)
    )


    # ---------------------------------------------------------
    # Lazy import
    # ---------------------------------------------------------

    try:

        from sentence_transformers import SentenceTransformer
        from qdrant_client import QdrantClient
        from qdrant_client.models import (
            VectorParams,
            Distance,
            PointStruct
        )


    except Exception as e:

        print(json.dumps({

            "status":"FAILED",
            "reason":"dependency_missing",
            "error":str(e)

        },indent=2))


    else:


        model_name="BAAI/bge-m3"


        print(
            "Loading embedding model:",
            model_name
        )


        model=SentenceTransformer(
            model_name
        )


        qdrant=QdrantClient(
            host="localhost",
            port=6333
        )


        vector_size=1024


        collections=[
            c.name
            for c in qdrant.get_collections().collections
        ]


        if collection not in collections:

            qdrant.create_collection(

                collection_name=collection,

                vectors_config=VectorParams(

                    size=vector_size,

                    distance=Distance.COSINE

                )

            )


        batch_size=32


        points=[]


        success=0


        for idx in range(
            0,
            len(chunks),
            batch_size
        ):

            batch=chunks[
                idx:
                idx+batch_size
            ]


            texts=[]


            for c in batch:

                if isinstance(c,dict):

                    text=c.get(
                        "text",
                        ""
                    )

                else:

                    text=str(c)


                texts.append(text)


            vectors=model.encode(
                texts,
                normalize_embeddings=True
            )


            for c,vec in zip(
                batch,
                vectors
            ):


                payload={}


                if isinstance(c,dict):

                    payload=c.copy()

                else:

                    payload={
                        "text":str(c)
                    }


                point=PointStruct(

                    id=str(uuid.uuid4()),

                    vector=vec.tolist(),

                    payload=payload

                )


                points.append(point)

                success+=1



            if len(points)>=128:


                qdrant.upsert(

                    collection_name=collection,

                    points=points

                )


                points=[]



        if points:

            qdrant.upsert(

                collection_name=collection,

                points=points

            )


        result={

            "timestamp":
            datetime.utcnow().isoformat()+"Z",

            "status":
            "EMBEDDING_INDEX_COMPLETE",

            "collection":
            collection,

            "chunks_input":
            len(chunks),

            "vectors_inserted":
            success

        }


        output=(
            ROOT+
            "/repository_data/mapping/"
            "embedding_index_result.json"
        )


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
echo "/workspace/delbot/repository_data/mapping/embedding_index_result.json"
echo "======================================================================"

echo

echo "PR-5.6 COMPLETE"

echo

echo "NEXT"
echo "PR-5.7 -> MVP Retrieval Engine Test"

echo

echo "Terminal remains open"

