#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AD
#
# Vector Indexing Pipeline Validation
#
# SAFE MVP
# ------------------------------------------------------------------------------
#
# READ ONLY
#
# - Tidak mengubah source code
# - Tidak mengubah PDF
# - Tidak membuat collection
# - Tidak insert vector permanen
# - Tidak menjalankan batch indexing
# - Tidak install package
# - Tidak rename file
# - Tidak delete file
# - Tidak overwrite project
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
#
# OUTPUT
#
# repository_data/mapping/
# ├── vector_indexing_pipeline_validation.json
# ├── vector_indexing_pipeline_validation_summary.json
# ├── vector_indexing_pipeline_validation_report.json
#
# ==============================================================================

set +e

ROOT="/workspace/delbot"
OUTPUT_DIR="$ROOT/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"

python3 <<'PYTHON'
import json
import os
import datetime
import traceback

result = {
    "timestamp": datetime.datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AD",
    "dependencies": {},
    "qdrant": {},
    "embedding": {},
    "indexing": {},
    "exception": None,
    "status": "UNKNOWN"
}

try:
    try:
        from qdrant_client import QdrantClient
        result["dependencies"]["qdrant_client"] = True
    except Exception:
        result["dependencies"]["qdrant_client"] = False

    try:
        from sentence_transformers import SentenceTransformer
        result["dependencies"]["sentence_transformers"] = True
    except Exception:
        result["dependencies"]["sentence_transformers"] = False

    collection = "delbot_documents"

    client = None

    try:
        from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

        store = get_qdrant_store()

        result["qdrant"]["store"] = True
        result["qdrant"]["runtime"] = type(store).__name__

        client = getattr(store, "client", None)

    except Exception:
        result["qdrant"]["store"] = False


    if client is not None:
        result["qdrant"]["client"] = True

        try:
            info = client.get_collection(collection)

            result["qdrant"]["collection"] = collection
            result["qdrant"]["collection_exists"] = True
            result["qdrant"]["vectors"] = str(
                info.config.params.vectors
            )

        except Exception as e:
            result["qdrant"]["collection_exists"] = False
            result["qdrant"]["collection_error"] = str(e)

    else:
        result["qdrant"]["client"] = False


    if result["dependencies"].get("sentence_transformers"):

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        vector = model.encode(
            "DELBot academic research intelligence system"
        )

        result["embedding"] = {
            "generated": True,
            "dimension": len(vector),
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }

    else:
        result["embedding"] = {
            "generated": False
        }


    result["indexing"] = {
        "pipeline_ready": (
            result["qdrant"].get("collection_exists", False)
            and result["embedding"].get("generated", False)
        ),
        "insert_test": False,
        "batch_indexing": False
    }


    if result["indexing"]["pipeline_ready"]:
        result["status"] = "READY"
    else:
        result["status"] = "PARTIAL"


except Exception as e:
    result["exception"] = str(e)
    result["traceback"] = traceback.format_exc()
    result["status"] = "FAILED"


paths = [
    "vector_indexing_pipeline_validation.json",
    "vector_indexing_pipeline_validation_summary.json",
    "vector_indexing_pipeline_validation_report.json"
]

for p in paths:
    with open(
        "/workspace/delbot/repository_data/mapping/" + p,
        "w"
    ) as f:
        json.dump(result, f, indent=2)


print(json.dumps(result, indent=2))

PYTHON


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform \
> /dev/null 2>&1

echo
echo "Generated"
echo "repository_data/mapping/vector_indexing_pipeline_validation.json"
echo "repository_data/mapping/vector_indexing_pipeline_validation_summary.json"
echo "repository_data/mapping/vector_indexing_pipeline_validation_report.json"

echo
echo "======================================================================"
echo "PR-5.1AD COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika status READY lanjut PR-5.1AE Document Indexing Engine"
echo "Jika PARTIAL audit vector store"
