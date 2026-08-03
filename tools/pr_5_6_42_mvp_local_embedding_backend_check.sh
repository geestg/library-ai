#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.42
#
# Local Embedding Backend Check
#
# MVP SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set -u

ROOT="/workspace/delbot"
OUTDIR="$ROOT/repository_data/mapping"
OUTPUT="$OUTDIR/local_embedding_backend_check.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.42 Local Embedding Backend Check"
echo "======================================================================"

python3 <<PY
import json
import platform
import importlib.util

backend=None
model=None

if importlib.util.find_spec("sentence_transformers"):
    backend="sentence_transformers"
    model="BAAI/bge-m3"

elif importlib.util.find_spec("FlagEmbedding"):
    backend="FlagEmbedding"
    model="BAAI/bge-m3"

result={
    "backend": backend,
    "model": model,
    "torch": importlib.util.find_spec("torch") is not None,
    "transformers": importlib.util.find_spec("transformers") is not None,
    "sentence_transformers": importlib.util.find_spec("sentence_transformers") is not None,
    "FlagEmbedding": importlib.util.find_spec("FlagEmbedding") is not None,
    "python": platform.python_version(),
    "status": "READY" if backend else "BACKEND_NOT_FOUND"
}

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
echo "READY -> PR-5.6.43 Local Embedding Build"
echo "BACKEND_NOT_FOUND -> install embedding backend"

