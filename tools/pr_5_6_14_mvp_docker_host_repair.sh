#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.14
#
# Docker Host Repair
#
# SAFE
#
# Tidak:
# - delete container
# - delete volume
# - migration
# - cleanup
# - rebuild
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_host_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.14 Docker Host Repair"
echo "======================================================================"

STARTED=false

if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl start docker >/dev/null 2>&1 || true
fi

if command -v service >/dev/null 2>&1; then
    sudo service docker start >/dev/null 2>&1 || true
fi

sleep 3

if docker info >/dev/null 2>&1; then
    STARTED=true
fi

python3 <<PY
import json
from datetime import datetime

started=${STARTED}

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "docker_ready":started,
    "status":"DOCKER_READY" if started else "DOCKER_NOT_READY",
    "next":"START_QDRANT" if started else "CHECK_HOST_MACHINE"
}

with open("${OUTPUT}","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "${OUTPUT}"
echo "======================================================================"

echo

echo "PR-5.6.14 COMPLETE"

echo

echo "NEXT"
echo "DOCKER_READY -> PR-5.6.15"
echo "DOCKER_NOT_READY -> Docker host/environment issue"

echo

