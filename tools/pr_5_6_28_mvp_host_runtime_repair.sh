#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.28
#
# Host Runtime Repair
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.28 Host Runtime Repair"
echo "======================================================================"

DOCKER_BIN=false
SOCKET_EXISTS=false
DOCKER_DAEMON=false
USER_IN_DOCKER_GROUP=false
QDRANT_PORT=false

command -v docker >/dev/null 2>&1 && DOCKER_BIN=true

[ -S /var/run/docker.sock ] && SOCKET_EXISTS=true

docker info >/dev/null 2>&1 && DOCKER_DAEMON=true

id -nG 2>/dev/null | grep -qw docker && USER_IN_DOCKER_GROUP=true

python3 - <<PY
import socket

ok=False
try:
    s=socket.create_connection(("127.0.0.1",6333),1)
    s.close()
    ok=True
except Exception:
    ok=False

print("TRUE" if ok else "FALSE")
PY
PORT_RESULT="$(python3 - <<'PY'
import socket
try:
    s=socket.create_connection(("127.0.0.1",6333),1)
    s.close()
    print("true")
except Exception:
    print("false")
PY
)"

[ "$PORT_RESULT" = "true" ] && QDRANT_PORT=true

STATUS="HOST_RUNTIME_REQUIRED"

if [ "$DOCKER_DAEMON" = true ]; then
    STATUS="START_QDRANT"
fi

if [ "$DOCKER_DAEMON" = true ] && [ "$QDRANT_PORT" = true ]; then
    STATUS="READY_FOR_PR_5_6_2"
fi

python3 - <<PY
import json

result={
    "docker_binary": ${DOCKER_BIN},
    "docker_socket": ${SOCKET_EXISTS},
    "docker_daemon": ${DOCKER_DAEMON},
    "user_in_docker_group": ${USER_IN_DOCKER_GROUP},
    "qdrant_port_6333": ${QDRANT_PORT},
    "status":"${STATUS}"
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
echo "NEXT"
echo "READY_FOR_PR_5_6_2 -> ulang PR-5.6.2"
echo "START_QDRANT -> start container qdrant"
echo "HOST_RUNTIME_REQUIRED -> perbaiki Docker Host"

