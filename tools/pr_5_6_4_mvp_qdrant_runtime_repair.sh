#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.4
#
# Qdrant Runtime Repair
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# - Check docker daemon
# - Start existing qdrant container
# - Create qdrant container if missing
#
# Tidak melakukan:
# - delete volume
# - delete collection
# - migration
# - cleanup
# - rebuild index
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
#

set -u

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/qdrant_runtime_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.4 Qdrant Runtime Repair"
echo "======================================================================"

python3 <<'PY'
import json
import subprocess
import urllib.request
from datetime import datetime


output="/workspace/delbot/repository_data/mapping/qdrant_runtime_repair.json"


result={
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "service":"qdrant",
    "status":"UNKNOWN"
}


def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            text=True
        ).strip()
    except Exception as e:
        return None


docker_check = run(["docker","info"])

if docker_check is None:
    result["status"]="DOCKER_NOT_READY"
    result["detail"]="docker daemon unavailable"

else:

    container = run([
        "docker",
        "ps",
        "-a",
        "--filter",
        "name=delbot-qdrant",
        "--format",
        "{{.Names}}"
    ])

    if container:

        run([
            "docker",
            "start",
            "delbot-qdrant"
        ])

        result["container"]="delbot-qdrant"
        result["action"]="START_EXISTING"

    else:

        run([
            "docker",
            "run",
            "-d",
            "--name",
            "delbot-qdrant",
            "-p",
            "6333:6333",
            "qdrant/qdrant"
        ])

        result["container"]="delbot-qdrant"
        result["action"]="CREATE_NEW"


    try:
        urllib.request.urlopen(
            "http://localhost:6333/healthz",
            timeout=5
        )

        result["health"]=True
        result["status"]="QDRANT_READY"

    except Exception as e:
        result["health"]=False
        result["status"]="QDRANT_STARTING"
        result["detail"]=str(e)


with open(output,"w") as f:
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
echo "QDRANT_READY -> run PR-5.6.2 embedding retry"
echo "QDRANT_STARTING -> wait then health check"

echo

echo "Terminal tetap terbuka"
