#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.18
#
# Docker Runtime Fix
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_runtime_fix.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.18 Docker Runtime Fix"
echo "======================================================================"

DOCKER_READY=false
QDRANT_READY=false
ACTION="NONE"

if command -v docker >/dev/null 2>&1; then

    if docker info >/dev/null 2>&1; then

        DOCKER_READY=true

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
            ACTION="DOCKER_STARTED"
        fi

    fi

fi

if [ "$DOCKER_READY" = true ]; then

    if docker ps -a --format '{{.Names}}' | grep -qx "delbot-qdrant"; then

        docker start delbot-qdrant >/dev/null 2>&1 || true

    else

        docker run -d \
            --name delbot-qdrant \
            -p 6333:6333 \
            -v delbot_qdrant_data:/qdrant/storage \
            qdrant/qdrant >/dev/null 2>&1 || true

    fi

    sleep 5

    python3 <<'PY'
import socket

sock = socket.socket()
sock.settimeout(2)

ok = False

try:
    sock.connect(("127.0.0.1",6333))
    ok = True
except Exception:
    ok = False

sock.close()

print("true" if ok else "false")
PY

    if python3 - <<'PY'
import socket,sys
s=socket.socket()
s.settimeout(2)
try:
    s.connect(("127.0.0.1",6333))
    sys.exit(0)
except:
    sys.exit(1)
PY
    then
        QDRANT_READY=true
    fi

fi

python3 <<PY
import json
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_ready": $DOCKER_READY,
    "qdrant_ready": $QDRANT_READY,
    "action": "$ACTION",
    "next": (
        "RUN_PR_5_6_2"
        if $QDRANT_READY
        else "FIX_HOST_RUNTIME"
    )
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
echo "PR-5.6.18 COMPLETE"

echo
echo "NEXT"
echo "RUN_PR_5_6_2"
echo "atau"
echo "FIX_HOST_RUNTIME"

echo
echo "Terminal remains open"

