#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BY
#
# MVP Deep PDF Source Scan
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Find missing PDF repository source.
#
# Scope:
# - Scan workspace
# - Scan repository_data
# - Scan dataset directories
# - Detect PDF files
# - Generate source mapping
#
# Tidak melakukan:
# - migration
# - cleanup
# - delete data
# - rebuild index
# - restart service
# - exit
#

set -u

ROOT="/workspace/delbot"
OUTPUT="/workspace/delbot/repository_data/mapping/mvp_deep_pdf_source_scan.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BY Deep PDF Source Scan"
echo "======================================================================"

python3 <<'PY'
import os
import json
from datetime import datetime

search_paths = [
    "/workspace/delbot",
    "/workspace",
    "/data",
    "/mnt/data",
    "/tmp"
]

pdf_files = []

ignored = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".cache"
}

for base in search_paths:
    if not os.path.exists(base):
        continue

    for root, dirs, files in os.walk(base):

        dirs[:] = [
            d for d in dirs
            if d not in ignored
        ]

        for file in files:
            if file.lower().endswith(".pdf"):
                full = os.path.join(root, file)

                pdf_files.append({
                    "path": full,
                    "size": os.path.getsize(full)
                })


result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "project": "DELBot MVP",
    "stage": "PR-5.1BY",
    "checks": {
        "workspace_scan": True,
        "pdf_found": len(pdf_files) > 0
    },
    "statistics": {
        "pdf_count": len(pdf_files)
    },
    "locations": pdf_files[:500],
    "status": (
        "PDF_SOURCE_FOUND"
        if len(pdf_files) > 0
        else "PDF_SOURCE_NOT_FOUND"
    )
}


output = "/workspace/delbot/repository_data/mapping/mvp_deep_pdf_source_scan.json"

with open(output, "w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))
PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.1BY COMPLETE"

echo

echo "NEXT"
echo "PDF_SOURCE_FOUND -> map repository PDF"
echo "PDF_SOURCE_NOT_FOUND -> inspect external dataset location"

echo

echo "Terminal remains open"
