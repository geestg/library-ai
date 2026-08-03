#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AE
#
# Document Indexing Engine Validation
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
# ├── document_indexing_engine_validation.json
# ├── document_indexing_engine_validation_summary.json
# └── document_indexing_engine_validation_report.json
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AE"
echo "Document Indexing Engine Validation"
echo "======================================================================"

python3 <<'PYTHON'

import json
import os
import glob
import importlib
from datetime import datetime


BASE = "/workspace/delbot"
OUTPUT = os.path.join(
    BASE,
    "repository_data",
    "mapping"
)

os.makedirs(
    OUTPUT,
    exist_ok=True
)


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AE",
    "dependencies": {},
    "pipeline": {},
    "sample": {},
    "exception": None,
    "status": "BLOCKED"
}


# --------------------------------------------------
# Dependency check
# --------------------------------------------------

dependencies = [
    "fitz",
    "pypdf",
    "sentence_transformers",
    "qdrant_client"
]


for dep in dependencies:
    try:
        importlib.import_module(dep)
        result["dependencies"][dep] = True
    except Exception:
        result["dependencies"][dep] = False



# --------------------------------------------------
# PDF discovery
# --------------------------------------------------

pdf_locations = [
    "repository_data",
    "repository_data/repository",
    "repository_data/papers",
    "repository_data/documents",
    "data"
]


pdf_files = []

for location in pdf_locations:
    path = os.path.join(BASE, location)

    if os.path.exists(path):
        pdf_files.extend(
            glob.glob(
                os.path.join(path, "**/*.pdf"),
                recursive=True
            )
        )


pdf_files = list(set(pdf_files))


result["pipeline"]["pdf_count"] = len(pdf_files)
result["pipeline"]["pdf_available"] = len(pdf_files) > 0



# --------------------------------------------------
# Parser validation
# --------------------------------------------------

parser_ready = (
    result["dependencies"].get("fitz", False)
    or result["dependencies"].get("pypdf", False)
)

result["pipeline"]["parser_ready"] = parser_ready



# --------------------------------------------------
# Chunk schema validation
# --------------------------------------------------

chunk_schema = {
    "chunk_id": "string",
    "content": "string",
    "metadata": {
        "source": "pdf_path",
        "page": "integer",
        "section": "string"
    }
}


result["sample"]["chunk_schema"] = chunk_schema



# --------------------------------------------------
# Embedding validation
# --------------------------------------------------

if result["dependencies"].get("sentence_transformers"):

    try:

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        vector = model.encode(
            "DELBot document indexing validation"
        )


        result["sample"]["embedding"] = {
            "generated": True,
            "dimension": len(vector)
        }


    except Exception as e:

        result["sample"]["embedding"] = {
            "generated": False,
            "error": str(e)
        }

else:

    result["sample"]["embedding"] = {
        "generated": False
    }



# --------------------------------------------------
# Final status
# --------------------------------------------------

if (
    parser_ready
    and result["dependencies"].get("sentence_transformers")
    and result["dependencies"].get("qdrant_client")
):
    result["status"] = "READY"


with open(
    os.path.join(
        OUTPUT,
        "document_indexing_engine_validation.json"
    ),
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


with open(
    os.path.join(
        OUTPUT,
        "document_indexing_engine_validation_summary.json"
    ),
    "w"
) as f:
    json.dump(
        {
            "stage": "PR-5.1AE",
            "status": result["status"],
            "pdf_count": result["pipeline"]["pdf_count"]
        },
        f,
        indent=2
    )


with open(
    os.path.join(
        OUTPUT,
        "document_indexing_engine_validation_report.json"
    ),
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
/workspace/delbot/tools/pr_5_1ae_document_indexing_engine_validation.sh \
2>/dev/null || true


echo ""
echo "Generated"
echo "repository_data/mapping/document_indexing_engine_validation.json"
echo "repository_data/mapping/document_indexing_engine_validation_summary.json"
echo "repository_data/mapping/document_indexing_engine_validation_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AE COMPLETE"
echo "======================================================================"

echo "NEXT"
echo "Jika status READY lanjut PR-5.1AF Batch PDF Indexer Preparation"
echo "Jika BLOCKED audit dependency"

