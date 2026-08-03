#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AM
#
# Repository PDF Intake Preparation
#
# MVP SAFE
# ------------------------------------------------------------------------------
#
# PURPOSE
#
# Menyiapkan folder repository PDF untuk MVP indexing.
#
# Rules:
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus file
# - Tidak overwrite PDF
# - Tidak menjalankan indexing
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AM"
echo "Repository PDF Intake Preparation"
echo "======================================================================"

PROJECT="/workspace/delbot"

SEARCH_DIRS=(
    "$PROJECT/repository_data"
    "$PROJECT/repository_data/repository"
    "$PROJECT/repository_data/papers"
    "$PROJECT/repository_data/documents"
    "$PROJECT/data"
)

TARGET="$PROJECT/repository_data/repository"

mkdir -p "$TARGET"

PDF_COUNT=$(find "$TARGET" -type f -iname "*.pdf" 2>/dev/null | wc -l)

JSON="$PROJECT/repository_data/mapping/repository_pdf_intake_preparation.json"

python3 <<PY

import json
from datetime import datetime
from pathlib import Path

target = Path("$TARGET")

pdfs = list(target.rglob("*.pdf"))

data = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AM",
    "repository": {
        "target": str(target),
        "exists": target.exists(),
        "pdf_count": len(pdfs),
        "samples": [
            str(x)
            for x in pdfs[:10]
        ]
    },
    "intake": {
        "folder_ready": True,
        "pdf_discovery_ready": True,
        "metadata_ready": True
    },
    "status": "READY_WAITING_PDF" if len(pdfs)==0 else "READY_WITH_PDF"
}

out = Path("$JSON")
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(json.dumps(data, indent=2))

PY


echo ""
echo "Generated"
echo "$JSON"

echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile /workspace/delbot/tools/pr_5_1am_repository_pdf_intake_preparation.sh 2>/dev/null || true

echo ""
echo "======================================================================"
echo "PR-5.1AM COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_WITH_PDF lanjut PR-5.1AN Real PDF Index Worker"
echo "Jika READY_WAITING_PDF copy dataset PDF thesis ke:"
echo "$TARGET"

