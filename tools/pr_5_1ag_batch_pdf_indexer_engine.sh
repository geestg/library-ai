#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AG
#
# Batch PDF Indexer Engine
#
# EXECUTION
# ------------------------------------------------------------------------------
#
# PDF
#   ->
# PyMuPDF Extraction
#   ->
# Chunk Builder
#   ->
# Embedding
#   ->
# Qdrant Collection
#
# SAFE MVP
# ------------------------------------------------------------------------------
#
# - Tidak exit
# - Tidak return
# - Terminal tetap terbuka
#
# ACTION
# ------------------------------------------------------------------------------
#
# Membuat index engine MVP.
#
# OUTPUT
#
# repository_data/mapping/
# ├── batch_pdf_indexer_engine.json
# ├── batch_pdf_indexer_engine_summary.json
# ├── batch_pdf_indexer_engine_report.json
#
# ==============================================================================


PROJECT="/workspace/delbot"

OUTPUT_DIR="$PROJECT/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"


echo "======================================================================"
echo "PR-5.1AG"
echo "Batch PDF Indexer Engine"
echo "======================================================================"


python3 <<'PYTHON'

import os
import json
import glob
import hashlib
from datetime import datetime


PROJECT="/workspace/delbot"

OUTPUT_DIR=os.path.join(
    PROJECT,
    "repository_data",
    "mapping"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AG",
    "engine": {
        "name": "batch_pdf_indexer_engine",
        "mode": "pdf_to_vector",
        "ready": False
    },
    "dependencies": {},
    "repository": {},
    "indexing": {
        "processed": 0,
        "chunks": 0,
        "vectors": 0
    },
    "exception": None
}


# ----------------------------------------------------------
# dependency check
# ----------------------------------------------------------

try:
    import fitz
    result["dependencies"]["pymupdf"] = True
except Exception:
    result["dependencies"]["pymupdf"] = False


try:
    from sentence_transformers import SentenceTransformer
    result["dependencies"]["sentence_transformers"] = True
except Exception:
    result["dependencies"]["sentence_transformers"] = False


try:
    from qdrant_client import QdrantClient
    result["dependencies"]["qdrant_client"] = True
except Exception:
    result["dependencies"]["qdrant_client"] = False


# ----------------------------------------------------------
# PDF discovery
# ----------------------------------------------------------

search_paths = [
    "repository_data",
    "repository_data/repository",
    "repository_data/papers",
    "repository_data/documents",
    "data",
    "storage"
]


pdf_files=[]


for path in search_paths:

    full=os.path.join(
        PROJECT,
        path
    )

    if os.path.exists(full):

        pdf_files.extend(
            glob.glob(
                full + "/**/*.pdf",
                recursive=True
            )
        )


pdf_files=list(
    sorted(
        set(pdf_files)
    )
)


result["repository"] = {
    "pdf_count": len(pdf_files),
    "sample": pdf_files[0] if pdf_files else None
}


# ----------------------------------------------------------
# Engine validation
# ----------------------------------------------------------

ready = all(
    result["dependencies"].values()
)


result["engine"]["ready"]=ready


# ----------------------------------------------------------
# MVP mode
#
# Tidak melakukan insert jika belum ada PDF
#
# ----------------------------------------------------------

if ready and len(pdf_files)==0:

    result["status"]="READY_WAITING_PDF"

elif ready:

    result["status"]="READY_EXECUTION_AVAILABLE"

else:

    result["status"]="BLOCKED_DEPENDENCY"



# ----------------------------------------------------------
# save report
# ----------------------------------------------------------

files = [
    "batch_pdf_indexer_engine.json",
    "batch_pdf_indexer_engine_summary.json",
    "batch_pdf_indexer_engine_report.json"
]


for file in files:

    with open(
        os.path.join(
            OUTPUT_DIR,
            file
        ),
        "w"
    ) as f:

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


PYTHON


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile \
/workspace/delbot/tools/pr_5_1ag_batch_pdf_indexer_engine.sh \
2>/dev/null || true


echo
echo "Generated"
echo "$OUTPUT_DIR/batch_pdf_indexer_engine.json"
echo "$OUTPUT_DIR/batch_pdf_indexer_engine_summary.json"
echo "$OUTPUT_DIR/batch_pdf_indexer_engine_report.json"


echo
echo "======================================================================"
echo "PR-5.1AG COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika READY_EXECUTION_AVAILABLE lanjut PR-5.1AH Batch PDF Index Execution"
echo "Jika READY_WAITING_PDF masukkan repository PDF MVP"
echo "======================================================================"

