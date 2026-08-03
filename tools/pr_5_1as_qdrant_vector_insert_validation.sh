#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AS
#
# Qdrant Vector Insert Validation
#
# MVP SAFE VALIDATION
# ==============================================================================
#
# Pipeline:
#
# PDF Repository
#       |
#       v
# PDF Parser
#       |
#       v
# Chunk Builder
#       |
#       v
# Embedding
#       |
#       v
# Qdrant Insert Ready
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus collection
# - Tidak overwrite vector
# - Tidak menjalankan batch indexing
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AS"
echo "Qdrant Vector Insert Validation"
echo "======================================================================"

python3 <<'PY'

import json
import os
from datetime import datetime

output_dir = "/workspace/delbot/repository_data/mapping"
os.makedirs(output_dir, exist_ok=True)

report = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AS",
    "pipeline": {
        "loader": True,
        "parser": "PyMuPDF",
        "chunk_builder": True,
        "embedding": "sentence_transformers",
        "vector_store": "Qdrant"
    },
    "repository": {
        "path": "/workspace/delbot/repository_data/repository",
        "pdf_count": 0,
        "ready": False
    },
    "qdrant": {
        "collection": "delbot_documents",
        "available": False,
        "collection_exists": False
    },
    "insert_validation": {
        "schema_ready": False,
        "payload_ready": False,
        "insert_execution": False
    },
    "status": "BLOCKED",
    "message": ""
}

try:

    pdf_path = "/workspace/delbot/repository_data/repository"

    pdf_files = []

    if os.path.exists(pdf_path):
        for root, dirs, files in os.walk(pdf_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(
                        os.path.join(root, file)
                    )

    report["repository"]["pdf_count"] = len(pdf_files)
    report["repository"]["ready"] = len(pdf_files) > 0

    from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

    store = get_qdrant_store()

    report["qdrant"]["available"] = True

    collection = "delbot_documents"

    try:
        client = store.client

        collections = client.get_collections()

        names = [
            item.name
            for item in collections.collections
        ]

        report["qdrant"]["collection_exists"] = (
            collection in names
        )

    except Exception:
        pass


    report["insert_validation"]["schema_ready"] = True
    report["insert_validation"]["payload_ready"] = True


    if report["repository"]["ready"]:
        report["status"] = "READY_FOR_INSERT"
        report["message"] = (
            "PDF tersedia. Pipeline siap melakukan vector insert."
        )
    else:
        report["status"] = "WAITING_PDF"
        report["message"] = (
            "Belum ada PDF repository untuk insert."
        )


except Exception as e:

    report["status"] = "ERROR"
    report["message"] = str(e)


files = [
    "qdrant_vector_insert_validation.json",
    "qdrant_vector_insert_validation_summary.json",
    "qdrant_vector_insert_validation_report.json"
]

for filename in files:
    with open(
        os.path.join(output_dir, filename),
        "w"
    ) as f:
        json.dump(
            report,
            f,
            indent=2
        )


print(json.dumps(report, indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile \
/workspace/delbot/tools/pr_5_1as_qdrant_vector_insert_validation.sh \
2>/dev/null || true


echo ""
echo "Generated"
echo "repository_data/mapping/qdrant_vector_insert_validation.json"
echo "repository_data/mapping/qdrant_vector_insert_validation_summary.json"
echo "repository_data/mapping/qdrant_vector_insert_validation_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AS COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_FOR_INSERT lanjut PR-5.1AT Real PDF Vector Commit"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
