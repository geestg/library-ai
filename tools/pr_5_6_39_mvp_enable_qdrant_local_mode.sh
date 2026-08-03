#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.39
#
# Enable Qdrant Local Mode
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
DBDIR="$ROOT/repository_data/qdrant_local"

mkdir -p "$OUTDIR"
mkdir -p "$DBDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.39 Enable Qdrant Local Mode"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

root=pathlib.Path("$ROOT")
db=root/"repository_data"/"qdrant_local"
mapping=root/"repository_data"/"mapping"

env=root/".env.mvp"

lines=[]

if env.exists():
    lines=env.read_text().splitlines()

cfg={}

for line in lines:
    if "=" in line:
        k,v=line.split("=",1)
        cfg[k.strip()]=v.strip()

cfg["DELBOT_VECTOR_BACKEND"]="QDRANT_LOCAL"
cfg["QDRANT_MODE"]="local"
cfg["QDRANT_PATH"]=str(db)
cfg["QDRANT_COLLECTION"]="delbot_mvp_documents"

with env.open("w") as f:
    for k,v in sorted(cfg.items()):
        f.write(f"{k}={v}\n")

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":"QDRANT_LOCAL",
    "database":str(db),
    "env_file":str(env),
    "status":"LOCAL_MODE_ENABLED"
}

outfile=mapping/"qdrant_local_mode.json"

outfile.write_text(json.dumps(result,indent=2))

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTDIR/qdrant_local_mode.json"
echo "======================================================================"

echo
echo "NEXT"
echo "PR-5.6.40 Local Embedding Index"

