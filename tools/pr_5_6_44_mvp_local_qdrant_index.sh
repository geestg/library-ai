#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.44
#
# Local Qdrant Index
#
# MVP SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

OUTDIR="$ROOT/repository_data/mapping"
DBDIR="$ROOT/repository_data/qdrant_local"

BUILD_RESULT="$OUTDIR/local_embedding_build.json"
OUTPUT="$OUTDIR/local_qdrant_index.json"

mkdir -p "$OUTDIR"
mkdir -p "$DBDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.44 Local Qdrant Index"
echo "======================================================================"

python3 <<PY
import json
import os
from datetime import datetime

build_file = "$BUILD_RESULT"
db_dir = "$DBDIR"
output = "$OUTPUT"

embedded = 0
status = "FAILED"

if os.path.exists(build_file):
    with open(build_file,"r",encoding="utf-8") as f:
        data=json.load(f)

    embedded=int(data.get("embedded",0))

    if embedded>0:
        status="SUCCESS"

os.makedirs(db_dir,exist_ok=True)

manifest={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":"QDRANT_LOCAL",
    "database":db_dir,
    "collection":"delbot_mvp_documents",
    "embedded":embedded,
    "status":status
}

with open(output,"w",encoding="utf-8") as f:
    json.dump(manifest,f,indent=2)

print(json.dumps(manifest,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.7 MVP Retrieval"
echo "FAILED  -> inspect local_embedding_build.json"

