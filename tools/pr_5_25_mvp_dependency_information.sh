#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.25
#
# Dependency Information
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
REPORTDIR="$ROOT/repository_data/report"
OUTPUT="$REPORTDIR/mvp_dependency_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.25 Dependency Information"
echo "======================================================================"

python3 <<PY
import json
import importlib.util
import pathlib
from datetime import datetime

report = pathlib.Path(r"$OUTPUT")

packages = [
    "fastapi",
    "uvicorn",
    "qdrant_client",
    "sentence_transformers",
    "transformers",
    "torch",
    "pymupdf",
    "numpy"
]

deps = {}

for pkg in packages:
    deps[pkg] = importlib.util.find_spec(pkg) is not None

summary = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "project": "DELBot MVP",
    "total_dependencies": len(packages),
    "available": sum(deps.values()),
    "missing": len(packages)-sum(deps.values()),
    "dependencies": deps,
    "status": "SUCCESS"
}

report.write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8"
)

print(json.dumps(summary, indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.26 MVP Storage Information"

