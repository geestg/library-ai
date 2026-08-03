#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.16
#
# Docker Host Fix
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_host_fix.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.16 Docker Host Fix"
echo "======================================================================"

DOCKER_READY=false
ACTION="NONE"

if command -v docker >/dev/null 2>&1; then

    if docker info >/dev/null 2>&1; then

        DOCKER_READY=true
        ACTION="ALREADY_RUNNING"

    else

        if command -v systemctl >/dev/null 2>&1; then
            sudo systemctl start docker >/dev/null 2>&1 || true
        fi

        if command -v service >/dev/null 2>&1; then
            sudo service docker start >/dev/null 2>&1 || true
        fi

        sleep 3

        if docker info >/dev/null 2>&1; then
            DOCKER_READY=true
            ACTION="STARTED"
        else
            ACTION="HOST_RUNTIME_REQUIRED"
        fi

    fi

fi

python3 <<PY
import json
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_ready": ${DOCKER_READY},
    "action": "${ACTION}",
    "next": (
        "START_QDRANT"
        if ${DOCKER_READY}
        else "FIX_HOST_DOCKER"
    )
}

with open("${OUTPUT}", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "${OUTPUT}"
echo "======================================================================"

echo
echo "PR-5.6.16 COMPLETE"

echo
echo "NEXT"
echo "START_QDRANT"
echo "FIX_HOST_DOCKER"

