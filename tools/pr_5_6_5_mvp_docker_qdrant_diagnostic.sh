#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.5
#
# Docker + Qdrant Diagnostic
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate docker runtime and qdrant availability
#
# Tidak melakukan:
# - delete
# - cleanup
# - migration
# - recreate volume
# - rebuild index
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
#

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/qdrant_diagnostic.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.5 Docker Qdrant Diagnostic"
echo "======================================================================"

python3 <<'PY'
import json
import subprocess
from datetime import datetime


def run(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip()[:500],
            "stderr": result.stderr.strip()[:500]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


docker_check = run("docker info")

container_check = run(
    "docker ps -a --filter name=delbot-qdrant --format '{{.Names}}'"
)

qdrant_check = run(
    "curl -s http://localhost:6333/healthz"
)


result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",

    "docker": docker_check,

    "qdrant_container": container_check,

    "qdrant_health": qdrant_check,

    "recommendation":
        "START_DOCKER_SERVICE"
        if not docker_check["success"]
        else
        "START_QDRANT_CONTAINER"
        if not qdrant_check["success"]
        else
        "QDRANT_READY"
}


with open(
    "/workspace/delbot/repository_data/mapping/qdrant_diagnostic.json",
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.5 COMPLETE"

echo
echo "NEXT:"
echo "START_DOCKER_SERVICE -> hidupkan docker daemon"
echo "START_QDRANT_CONTAINER -> start container"
echo "QDRANT_READY -> lanjut PR-5.6.2"

echo
echo "Terminal tetap terbuka"
