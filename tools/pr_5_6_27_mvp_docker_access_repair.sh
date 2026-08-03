#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.27
#
# Docker Access Repair
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_access_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.27 Docker Access Repair"
echo "======================================================================"

DOCKER_BIN=false
SOCKET=false
GROUP_EXISTS=false
USER_IN_GROUP=false
DOCKER_DAEMON=false
ACTION="NONE"

command -v docker >/dev/null 2>&1 && DOCKER_BIN=true

[ -S /var/run/docker.sock ] && SOCKET=true

if getent group docker >/dev/null 2>&1; then
    GROUP_EXISTS=true
fi

if id -nG 2>/dev/null | tr ' ' '\n' | grep -qx docker; then
    USER_IN_GROUP=true
fi

if docker info >/dev/null 2>&1; then
    DOCKER_DAEMON=true
fi

if [ "$GROUP_EXISTS" = true ] && [ "$USER_IN_GROUP" = false ]; then
    sudo usermod -aG docker "$USER" >/dev/null 2>&1 || true

    if id -nG 2>/dev/null | tr ' ' '\n' | grep -qx docker; then
        USER_IN_GROUP=true
    else
        ACTION="RELOGIN_REQUIRED"
    fi
fi

if docker info >/dev/null 2>&1; then
    DOCKER_DAEMON=true
fi

STATUS="READY"

if [ "$DOCKER_BIN" = false ]; then
    STATUS="DOCKER_NOT_INSTALLED"
elif [ "$SOCKET" = false ]; then
    STATUS="DOCKER_SOCKET_NOT_FOUND"
elif [ "$GROUP_EXISTS" = false ]; then
    STATUS="DOCKER_GROUP_NOT_FOUND"
elif [ "$USER_IN_GROUP" = false ]; then
    STATUS="USER_NOT_IN_DOCKER_GROUP"
elif [ "$DOCKER_DAEMON" = false ]; then
    STATUS="DOCKER_DAEMON_DOWN"
fi

python3 <<PY
import json

result = {
    "docker_binary": ${DOCKER_BIN},
    "docker_socket": ${SOCKET},
    "docker_group_exists": ${GROUP_EXISTS},
    "user_in_docker_group": ${USER_IN_GROUP},
    "docker_daemon": ${DOCKER_DAEMON},
    "action": "${ACTION}",
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
echo "READY -> PR-5.6.2"
echo "USER_NOT_IN_DOCKER_GROUP -> newgrp docker / login ulang"
echo "DOCKER_DAEMON_DOWN -> hidupkan Docker Host"

