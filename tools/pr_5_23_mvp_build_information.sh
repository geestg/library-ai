#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.23
#
# Build Information
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

OUTPUT="$REPORTDIR/mvp_build_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.23 Build Information"
echo "======================================================================"

python3 <<PY
import json
import pathlib
import platform
import subprocess
from datetime import datetime

root=pathlib.Path(r"$ROOT")
output=pathlib.Path(r"$OUTPUT")

def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
    except Exception:
        return "UNKNOWN"

info={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "version":"0.1.0-mvp",
    "build_type":"MVP",
    "python":platform.python_version(),
    "platform":platform.system(),
    "architecture":platform.machine(),
    "git_commit":run(["git","-C",str(root),"rev-parse","--short","HEAD"]),
    "git_branch":run(["git","-C",str(root),"branch","--show-current"]),
    "status":"SUCCESS"
}

output.write_text(
    json.dumps(info,indent=2),
    encoding="utf-8"
)

print(json.dumps(info,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.24 MVP Environment Information"

