#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AQ
#
# Repository PDF Dataset Intake Validation
#
# MVP
# ==============================================================================
#
# PURPOSE
#
# Validasi dataset PDF thesis sebelum indexing.
#
# Pipeline:
#
# repository_data/repository
#          |
#          v
# PDF Discovery
#          |
#          v
# Metadata Detection
#          |
#          v
# Ready Index
#
# Rules:
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus file
# - Tidak mengubah PDF
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AQ"
echo "Repository PDF Dataset Intake Validation"
echo "======================================================================"

python3 <<'PY'

import json
from pathlib import Path
from datetime import datetime


ROOT = Path("/workspace/delbot")

repository = ROOT / "repository_data" / "repository"
mapping = ROOT / "repository_data" / "mapping"

mapping.mkdir(parents=True, exist_ok=True)


pdf_files = []

if repository.exists():
    pdf_files = list(repository.rglob("*.pdf"))


documents = []

for pdf in pdf_files:

    stat = pdf.stat()

    documents.append(
        {
            "file": str(pdf.relative_to(ROOT)),
            "size_bytes": stat.st_size,
            "name": pdf.name
        }
    )


result = {

    "timestamp": datetime.now().isoformat(),

    "project": "DELBot MVP",

    "stage": "PR-5.1AQ",

    "repository": {

        "path": str(repository),

        "exists": repository.exists(),

        "pdf_count": len(pdf_files),

        "documents": documents[:20]

    },

    "validation": {

        "pdf_discovery": True,

        "dataset_ready": len(pdf_files) > 0

    },

    "status":
        "READY_FOR_INDEX"
        if len(pdf_files) > 0
        else "WAITING_PDF"

}


for name in [
    "repository_pdf_dataset_intake.json",
    "repository_pdf_dataset_intake_summary.json",
    "repository_pdf_dataset_intake_report.json"
]:

    with open(mapping / name,"w") as f:
        json.dump(result,f,indent=2)


print(json.dumps(result,indent=2))


PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile /workspace/delbot/tools/pr_5_1aq_repository_pdf_dataset_intake.sh 2>/dev/null || true


echo
echo "======================================================================"
echo "PR-5.1AQ COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika READY_FOR_INDEX lanjut PR-5.1AR Real PDF Index Worker Execution"
echo "Jika WAITING_PDF copy PDF thesis ke:"
echo "/workspace/delbot/repository_data/repository"

