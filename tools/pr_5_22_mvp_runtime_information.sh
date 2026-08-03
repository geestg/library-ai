#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.22
#
# Runtime Information
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
OUTPUT="$REPORTDIR/mvp_runtime_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.22 Runtime Information"
echo "======================================================================"

python3 <<PY
import json
import os
import platform
import pathlib
from datetime import datetime

root=pathlib.Path(r"$ROOT")
out=pathlib.Path(r"$OUTPUT")

runtime={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "python_version":platform.python_version(),
    "platform":platform.system(),
    "platform_release":platform.release(),
    "architecture":platform.machine(),
    "hostname":platform.node(),
    "working_directory":str(root),
    "venv":os.environ.get("VIRTUAL_ENV"),
    "gpu_available":False,
    "gpu_name":None,
    "cuda_available":False,
    "status":"SUCCESS"
}

try:
    import torch
    runtime["cuda_available"]=bool(torch.cuda.is_available())

    if runtime["cuda_available"]:
        runtime["gpu_available"]=True
        runtime["gpu_name"]=torch.cuda.get_device_name(0)
except Exception:
    pass

out.write_text(
    json.dumps(runtime,indent=2),
    encoding="utf-8"
)

summary={
    "project":runtime["project"],
    "python":runtime["python_version"],
    "platform":runtime["platform"],
    "gpu_available":runtime["gpu_available"],
    "status":"SUCCESS"
}

print(json.dumps(summary,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.23 MVP Build Information"

