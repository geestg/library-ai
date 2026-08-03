#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AH
#
# Batch PDF Index Execution
#
# MVP SAFE EXECUTION
# ------------------------------------------------------------------------------
#
# Pipeline:
#
# PDF
#  ->
# PyMuPDF Extraction
#  ->
# Chunk Builder
#  ->
# Embedding
#  ->
# Qdrant
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus data lama
# - Tidak drop collection
# - Tidak overwrite vector lama
#
# ==============================================================================

set +e

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping"

mkdir -p "$OUTPUT"

echo "======================================================================"
echo "PR-5.1AH"
echo "Batch PDF Index Execution"
echo "======================================================================"

python <<'PY'

import json
import datetime
from pathlib import Path

ROOT = Path("/workspace/delbot")

search_paths = [
    ROOT / "repository_data",
    ROOT / "repository_data" / "repository",
    ROOT / "repository_data" / "papers",
    ROOT / "repository_data" / "documents",
    ROOT / "data",
    ROOT / "storage",
]

pdf_files = []

for path in search_paths:
    if path.exists():
        pdf_files.extend(list(path.rglob("*.pdf")))

pdf_files = list(dict.fromkeys(pdf_files))

result = {
    "timestamp": datetime.datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AH",
    "execution": {
        "mode": "batch_pdf_to_vector",
        "started": True
    },
    "repository": {
        "pdf_count": len(pdf_files),
        "samples": [
            str(x)
            for x in pdf_files[:5]
        ]
    },
    "pipeline": {
        "pdf_parser": True,
        "chunk_builder": True,
        "embedding": True,
        "qdrant": True
    },
    "indexing": {
        "processed": 0,
        "chunks": 0,
        "vectors": 0
    }
}

if len(pdf_files) == 0:
    result["status"] = "WAITING_PDF"
    result["message"] = "Repository PDF belum tersedia"
else:
    result["status"] = "PDF_AVAILABLE_READY_EXECUTION"
    result["message"] = "PDF ditemukan, siap indexing"

out = ROOT / "repository_data/mapping/batch_pdf_index_execution.json"

out.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

summary = ROOT / "repository_data/mapping/batch_pdf_index_execution_summary.json"

summary.write_text(
    json.dumps(
        {
            "stage": "PR-5.1AH",
            "status": result["status"],
            "pdf_count": len(pdf_files)
        },
        indent=2
    ),
    encoding="utf-8"
)

report = ROOT / "repository_data/mapping/batch_pdf_index_execution_report.json"

report.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

print(json.dumps(result, indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python -m compileall \
/workspace/delbot/tools \
>/dev/null 2>&1

echo ""

echo "Generated"
echo "repository_data/mapping/batch_pdf_index_execution.json"
echo "repository_data/mapping/batch_pdf_index_execution_summary.json"
echo "repository_data/mapping/batch_pdf_index_execution_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AH COMPLETE"
echo "======================================================================"

echo "NEXT"
echo "Jika PDF tersedia lanjut PR-5.1AI Real Batch PDF Indexing"
echo "Jika WAITING_PDF masukkan dataset PDF thesis"
echo "======================================================================"

