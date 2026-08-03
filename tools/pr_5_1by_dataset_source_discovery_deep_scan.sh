#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BY
#
# Dataset Source Discovery Deep Scan
#
# MVP SAFE
# ==============================================================================

set -u

PROJECT_ROOT="/workspace/delbot"
OUTPUT_DIR="/workspace/delbot/repository_data/mapping"
OUTPUT_FILE="${OUTPUT_DIR}/mvp_dataset_source_discovery.json"

mkdir -p "${OUTPUT_DIR}"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BY Dataset Source Discovery Deep Scan"
echo "======================================================================"

python3 <<'PYTHON'
import os
import json
from datetime import datetime

scan_targets = [
    "/workspace/delbot",
    "/workspace",
    "/data",
    "/mnt",
    "/tmp"
]

pdf_locations = []
repository_candidates = []
pdf_count = 0

visited = set()

for target in scan_targets:
    if not os.path.exists(target):
        continue

    for root, dirs, files in os.walk(target):

        if root in visited:
            continue

        visited.add(root)

        lower_root = root.lower()

        if any(
            keyword in lower_root
            for keyword in [
                "repository",
                "dataset",
                "thesis",
                "skripsi",
                "paper",
                "document",
                "pdf"
            ]
        ):
            repository_candidates.append(root)

        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_count += 1

                full_path = os.path.join(root, file)

                pdf_locations.append({
                    "path": full_path,
                    "size": os.path.getsize(full_path)
                })

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "project": "DELBot MVP",
    "stage": "PR-5.1BY",
    "scan_targets": scan_targets,
    "checks": {
        "workspace_scan": True,
        "pdf_found": pdf_count > 0,
        "repository_candidate_found": len(repository_candidates) > 0
    },
    "statistics": {
        "pdf_count": pdf_count,
        "repository_candidates": len(repository_candidates)
    },
    "pdf_locations": pdf_locations[:200],
    "repository_candidates": repository_candidates[:200],
    "status": (
        "PDF_SOURCE_FOUND"
        if pdf_count > 0
        else "PDF_SOURCE_NOT_FOUND"
    )
}

output = "/workspace/delbot/repository_data/mapping/mvp_dataset_source_discovery.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))

print()
print("======================================================================")
print("Generated")
print(output)
print("======================================================================")

if pdf_count > 0:
    print("PR-5.1BY COMPLETE")
    print()
    print("NEXT")
    print("READY_PDF_SOURCE -> lanjut PR-5.1BZ PDF Repository Binding")
else:
    print("PR-5.1BY BLOCKED")
    print()
    print("NEXT")
    print("PDF source masih belum ditemukan")
PYTHON


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
    /workspace/delbot/delbot_platform \
    -q

echo
echo "======================================================================"
echo "Terminal remains open"
echo "======================================================================"
