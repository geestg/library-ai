#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.34
#
# Runtime Capability Report
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/runtime_capability_report.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.34 Runtime Capability Report"
echo "======================================================================"

INSIDE_CONTAINER=false
DOCKER_BIN=false
DOCKER_SOCKET=false
DOCKER_DAEMON=false
DOCKERD_BIN=false
DOCKERD_RUNNING=false

[ -f /.dockerenv ] && INSIDE_CONTAINER=true

command -v docker >/dev/null 2>&1 && DOCKER_BIN=true

command -v dockerd >/dev/null 2>&1 && DOCKERD_BIN=true

[ -S /var/run/docker.sock ] && DOCKER_SOCKET=true

docker info >/dev/null 2>&1
[ $? -eq 0 ] && DOCKER_DAEMON=true

pgrep -x dockerd >/dev/null 2>&1
[ $? -eq 0 ] && DOCKERD_RUNNING=true

STATUS="HOST_RUNTIME_REQUIRED"

if [ "$DOCKER_DAEMON" = true ]; then
    STATUS="DOCKER_READY"
fi

python3 <<PY
import json

result = {
    "inside_container": ${INSIDE_CONTAINER},
    "docker_binary": ${DOCKER_BIN},
    "dockerd_binary": ${DOCKERD_BIN},
    "docker_socket": ${DOCKER_SOCKET},
    "docker_daemon": ${DOCKER_DAEMON},
    "dockerd_running": ${DOCKERD_RUNNING},
    "status": "${STATUS}"
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
echo "NEXT"
echo "DOCKER_READY -> ulang PR-5.6.2"
echo "HOST_RUNTIME_REQUIRED -> jalankan Docker daemon dari host"

