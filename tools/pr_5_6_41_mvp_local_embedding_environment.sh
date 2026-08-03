#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.41
#
# Local Embedding Environment
#
# MVP SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"
OUTDIR="$ROOT/repository_data/mapping"
OUTPUT="$OUTDIR/local_embedding_environment.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.41 Local Embedding Environment"
echo "======================================================================"

python3 <<PY
import json
import os
import subprocess
import sys
import importlib.util

result = {
    "backend": "QDRANT_LOCAL",
    "python": sys.version.split()[0]
}

def installed(name):
    return importlib.util.find_spec(name) is not None

packages = {
    "sentence_transformers":"sentence-transformers",
    "transformers":"transformers",
    "torch":"torch",
    "qdrant_client":"qdrant-client"
}

installed_before = {}

for m in packages:
    installed_before[m] = installed(m)

for module,pipname in packages.items():
    if not installed(module):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-q",
                pipname
            ],
            check=False
        )

installed_after = {}

for m in packages:
    installed_after[m] = installed(m)

result["installed_before"] = installed_before
result["installed_after"] = installed_after

if all(installed_after.values()):
    result["status"]="READY"
else:
    result["status"]="FAILED"

with open("$OUTPUT","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "READY -> PR-5.6.42 Local Embedding Index"
echo "FAILED -> cek koneksi internet / pip"

