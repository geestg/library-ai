#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.25
#
# Host Runtime Final Diagnosis
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_final_diagnosis.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.25 Host Runtime Final Diagnosis"
echo "======================================================================"

DOCKER_BINARY=0
DOCKER_SOCKET=0
DOCKER_DAEMON=0
QDRANT_PORT=0

command -v docker >/dev/null 2>&1 && DOCKER_BINARY=1

[ -S /var/run/docker.sock ] && DOCKER_SOCKET=1

docker info >/dev/null 2>&1 && DOCKER_DAEMON=1

python3 - <<PY
import socket
q=0
try:
    s=socket.create_connection(("127.0.0.1",6333),2)
    s.close()
    q=1
except Exception:
    pass

print(q)
PY
QDRANT_PORT=$(python3 - <<'PY'
import socket
try:
    s=socket.create_connection(("127.0.0.1",6333),2)
    s.close()
    print(1)
except Exception:
    print(0)
PY
)

STATUS="HOST_RUNTIME_REQUIRED"

if [ "$DOCKER_DAEMON" -eq 1 ]; then
    STATUS="DOCKER_READY"
fi

if [ "$DOCKER_DAEMON" -eq 1 ] && [ "$QDRANT_PORT" -eq 1 ]; then
    STATUS="QDRANT_READY"
fi

python3 - <<PY
import json

result={
    "docker_binary": bool($DOCKER_BINARY),
    "docker_socket": bool($DOCKER_SOCKET),
    "docker_daemon": bool($DOCKER_DAEMON),
    "qdrant_port_6333": bool($QDRANT_PORT),
    "status":"$STATUS"
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
echo "QDRANT_READY -> Run PR-5.6.2"
echo "DOCKER_READY -> Start Qdrant"
echo "HOST_RUNTIME_REQUIRED -> Fix Host Docker"

