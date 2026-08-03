#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.24
#
# Environment Information
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
OUTPUT="$REPORTDIR/mvp_environment_information.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.24 Environment Information"
echo "======================================================================"

ROOT="$ROOT" OUTPUT="$OUTPUT" python3 <<'PY'
import json
import os
import pathlib
import platform
import subprocess
from datetime import datetime

root = pathlib.Path(os.environ["ROOT"])
output = pathlib.Path(os.environ["OUTPUT"])

def cmd(command):
    try:
        return subprocess.check_output(
            command,
            shell=True,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return ""

venv = os.environ.get("VIRTUAL_ENV", "")

data = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "project": "DELBot MVP",
    "workspace": str(root),
    "python_version": platform.python_version(),
    "python_executable": cmd("which python3"),
    "virtualenv": venv if venv else None,
    "os": platform.system(),
    "os_release": platform.release(),
    "hostname": platform.node(),
    "user": cmd("whoami"),
    "shell": os.environ.get("SHELL"),
    "status": "SUCCESS"
}

output.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(json.dumps({
    "project": data["project"],
    "python": data["python_version"],
    "virtualenv": bool(data["virtualenv"]),
    "os": data["os"],
    "user": data["user"],
    "status": data["status"]
}, indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.25 MVP Dependency Information"

