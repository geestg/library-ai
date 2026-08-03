#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.1
#
# Qdrant Bootstrap Health Check
#
# MVP SAFE
# ==============================================================================

set -u

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.1 Qdrant Bootstrap"
echo "======================================================================"

QDRANT_CONTAINER="delbot-qdrant"
QDRANT_PORT="6333"
OUTPUT="/workspace/delbot/repository_data/mapping/qdrant_health.json"


mkdir -p "$(dirname "$OUTPUT")"


python3 <<'PY'
import json
import subprocess
import urllib.request
from datetime import datetime


container="delbot-qdrant"
port=6333
status="UNKNOWN"
detail=""


def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT
        ).decode()
    except Exception:
        return ""


# check health
try:
    urllib.request.urlopen(
        "http://localhost:6333/healthz",
        timeout=3
    )

    status="RUNNING"
    detail="existing qdrant healthy"

except Exception:

    containers = run([
        "docker",
        "ps",
        "-a",
        "--format",
        "{{.Names}}"
    ])


    if container in containers.splitlines():

        run([
            "docker",
            "start",
            container
        ])

        status="STARTED"
        detail="existing container started"


    else:

        run([
            "docker",
            "run",
            "-d",
            "--name",
            container,
            "-p",
            "6333:6333",
            "-v",
            "/workspace/delbot/qdrant_storage:/qdrant/storage",
            "qdrant/qdrant"
        ])

        status="CREATED"
        detail="new qdrant container created"



result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "service":"qdrant",
    "container":container,
    "port":port,
    "status":status,
    "detail":detail
}


with open(
    "/workspace/delbot/repository_data/mapping/qdrant_health.json",
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result,indent=2))

PY


echo
echo "======================================================================"
echo "Health output:"
echo "/workspace/delbot/repository_data/mapping/qdrant_health.json"
echo "======================================================================"

echo
echo "PR-5.6.1 COMPLETE"

echo
echo "NEXT"
echo "Run PR-5.6 embedding index again"

echo
echo "Terminal remains open"
