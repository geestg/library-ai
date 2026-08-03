#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BW
#
# MVP Dataset Index Repair
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Repair dataset index mapping only.
#
# Scope:
# - Detect PDF repository
# - Detect chunk dataset
# - Detect embedding dataset
# - Build dataset availability map
#
# Tidak melakukan:
# - migration
# - cleanup
# - delete data
# - restart service
# - exit
#

set -u

ROOT="/workspace/delbot"
REPO_DATA="${ROOT}/repository_data"
MAPPING_DIR="${REPO_DATA}/mapping"

mkdir -p "${MAPPING_DIR}"

OUTPUT="${MAPPING_DIR}/mvp_dataset_index_repair.json"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BW Dataset Index Repair"
echo "======================================================================"

python3 <<'PY'
import json
import os
from datetime import datetime, timezone

ROOT="/workspace/delbot"
REPO_DATA=f"{ROOT}/repository_data"
OUTPUT=f"{REPO_DATA}/mapping/mvp_dataset_index_repair.json"

result = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BW",
    "checks": {},
    "statistics": {},
    "status": ""
}

pdf_locations = []
chunk_locations = []
embedding_locations = []

for base, dirs, files in os.walk(REPO_DATA):

    for f in files:
        path=os.path.join(base,f)

        if f.lower().endswith(".pdf"):
            pdf_locations.append(path)

        if "chunk" in f.lower():
            chunk_locations.append(path)

        if "embedding" in f.lower() or f.lower().endswith(".bin"):
            embedding_locations.append(path)


result["statistics"] = {
    "pdf_count": len(pdf_locations),
    "chunk_count": len(chunk_locations),
    "embedding_count": len(embedding_locations)
}


result["checks"] = {
    "repository_data": os.path.exists(REPO_DATA),
    "pdf_repository_available": len(pdf_locations) > 0,
    "chunk_dataset_available": len(chunk_locations) > 0,
    "embedding_dataset_available": len(embedding_locations) > 0
}


result["dataset_flow"] = {
    "pdf_to_chunk": len(pdf_locations) > 0 and len(chunk_locations) > 0,
    "chunk_to_embedding": len(chunk_locations) > 0 and len(embedding_locations) > 0,
    "dataset_ready_for_query": (
        len(pdf_locations) > 0
        and len(chunk_locations) > 0
        and len(embedding_locations) > 0
    )
}


if result["dataset_flow"]["dataset_ready_for_query"]:
    result["status"]="READY_DATASET_INDEX"
else:
    result["status"]="INCOMPLETE_DATASET_INDEX"


with open(OUTPUT,"w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))

PY

echo
echo "======================================================================"
echo "Generated"
echo "${OUTPUT}"
echo "======================================================================"

echo
echo "PR-5.1BW COMPLETE"
echo

echo "NEXT"

echo "READY_DATASET_INDEX -> rerun PR-5.1BV MVP Live Query Validation"
echo "INCOMPLETE_DATASET_INDEX -> locate missing dataset source"

echo
echo "Terminal remains open"
