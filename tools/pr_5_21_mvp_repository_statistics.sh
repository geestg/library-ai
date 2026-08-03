#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.21
#
# Repository Statistics
#
# SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

MAPDIR="$ROOT/repository_data/mapping"
REPORTDIR="$ROOT/repository_data/report"

OUTPUT="$REPORTDIR/mvp_repository_statistics.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.21 Repository Statistics"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

root=pathlib.Path(r"$ROOT")
report=pathlib.Path(r"$OUTPUT")

stats={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":"QDRANT_LOCAL",
    "pdf_documents":0,
    "chunk_count":0,
    "indexed_vectors":0,
    "collections":1,
    "status":"SUCCESS"
}

pdf_dir=root/"delbot_platform"/"repository_data"/"pdf"

if pdf_dir.exists():
    stats["pdf_documents"]=len(list(pdf_dir.glob("*.pdf")))

chunk_file=root/"repository_data"/"mapping"/"pdf_chunk_manifest.json"

if chunk_file.exists():
    try:
        data=json.loads(chunk_file.read_text())

        if isinstance(data,list):
            stats["chunk_count"]=len(data)

        elif isinstance(data,dict):
            stats["chunk_count"]=(
                data.get("chunks")
                or data.get("chunk_count")
                or len(data.get("items",[]))
            )

    except Exception:
        pass

retrieval=root/"repository_data"/"mapping"/"local_retrieval_engine.json"

if retrieval.exists():
    try:
        r=json.loads(retrieval.read_text())
        stats["indexed_vectors"]=r.get("indexed_points",0)
    except Exception:
        pass

report.write_text(
    json.dumps(stats,indent=2),
    encoding="utf-8"
)

print(json.dumps(stats,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.22 MVP Runtime Information"

