#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.23
#
# Host Runtime Bootstrap
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_bootstrap.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.23 Host Runtime Bootstrap"
echo "======================================================================"

docker_before=false
docker_after=false
socket=false
qdrant=false

[ -S /var/run/docker.sock ] && socket=true

docker info >/dev/null 2>&1 && docker_before=true

if [ "$docker_before" = false ]; then

    sudo systemctl start docker >/dev/null 2>&1 || true

    sudo service docker start >/dev/null 2>&1 || true

fi

docker info >/dev/null 2>&1 && docker_after=true

if [ "$docker_after" = true ]; then

    docker start delbot-qdrant >/dev/null 2>&1 || true

    docker ps --format '{{.Names}}' \
        | grep -qx delbot-qdrant \
        && qdrant=true

fi

python3 <<PY
import json
import socket

status="HOST_RUNTIME_REQUIRED"

if $docker_after:
    status="DOCKER_READY"

if $docker_after and $qdrant:
    try:
        s=socket.create_connection(("127.0.0.1",6333),2)
        s.close()
        status="QDRANT_READY"
    except Exception:
        status="START_QDRANT"

result={
    "docker_socket": $socket,
    "docker_before": $docker_before,
    "docker_after": $docker_after,
    "qdrant_container": $qdrant,
    "status": status
}

with open("$OUTPUT","w") as f:
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
echo "QDRANT_READY -> ulang PR-5.6.2"
echo "START_QDRANT -> docker logs delbot-qdrant"
echo "HOST_RUNTIME_REQUIRED -> hidupkan Docker Desktop / Docker Engine pada host"

