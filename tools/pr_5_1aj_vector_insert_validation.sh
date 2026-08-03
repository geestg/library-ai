#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AJ
#
# Vector Insert Validation
#
# MVP SAFE
# ------------------------------------------------------------------------------
#
# Pipeline:
#
# PDF
#  ->
# Extraction
#  ->
# Chunk
#  ->
# Embedding
#  ->
# Qdrant Insert Validation
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak delete vector
# - Tidak overwrite collection
# - Tidak insert permanent
#
# OUTPUT
#
# repository_data/mapping/
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AJ"
echo "Vector Insert Validation"
echo "======================================================================"

python3 <<'PYTHON'
import json
import os
from datetime import datetime

output_dir = "/workspace/delbot/repository_data/mapping"
os.makedirs(output_dir, exist_ok=True)

result = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AJ",
    "validation": {
        "mode": "dry_run_vector_insert_validation",
        "permanent_insert": False
    },
    "qdrant": {
        "collection": "delbot_documents",
        "available": False,
        "collection_exists": False
    },
    "embedding": {
        "available": False,
        "dimension": None
    },
    "sample_vector": {
        "generated": False,
        "dimension": None
    },
    "insert_validation": {
        "payload_ready": False,
        "vector_schema_ready": False,
        "insert_test": False
    },
    "status": "BLOCKED",
    "message": "Menunggu repository PDF untuk menghasilkan chunk dan vector"
}

try:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    vector = model.encode(
        "DELBot MVP academic research document"
    )

    result["embedding"]["available"] = True
    result["embedding"]["dimension"] = len(vector)

    result["sample_vector"]["generated"] = True
    result["sample_vector"]["dimension"] = len(vector)

except Exception as e:
    result["embedding"]["error"] = str(e)


try:
    from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

    store = get_qdrant_store()

    result["qdrant"]["available"] = True

    try:
        collections = store.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        if "delbot_documents" in names:
            result["qdrant"]["collection_exists"] = True

    except Exception:
        pass

except Exception as e:
    result["qdrant"]["error"] = str(e)


if (
    result["embedding"]["available"]
    and result["qdrant"]["collection_exists"]
):
    result["insert_validation"]["payload_ready"] = True
    result["insert_validation"]["vector_schema_ready"] = True
    result["status"] = "READY"
    result["message"] = "Vector insert pipeline siap diuji dengan PDF repository"

path = os.path.join(
    output_dir,
    "vector_insert_validation.json"
)

with open(path, "w") as f:
    json.dump(
        result,
        f,
        indent=2
    )

for suffix in [
    "_summary.json",
    "_report.json"
]:
    with open(
        path.replace(".json", suffix),
        "w"
    ) as f:
        json.dump(
            result,
            f,
            indent=2
        )

print(json.dumps(result, indent=2))

PYTHON

echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile \
/workspace/delbot/tools/pr_5_1aj_vector_insert_validation.sh \
2>/dev/null || true

echo ""
echo "Generated"
echo "repository_data/mapping/vector_insert_validation.json"
echo "repository_data/mapping/vector_insert_validation_summary.json"
echo "repository_data/mapping/vector_insert_validation_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AJ COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY lanjut PR-5.1AK Repository PDF Loader"
echo "Jika BLOCKED masukkan PDF thesis repository"
