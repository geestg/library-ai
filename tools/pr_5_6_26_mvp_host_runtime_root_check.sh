#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.26
#
# Host Runtime Root Check
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_root_check.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.26 Host Runtime Root Check"
echo "======================================================================"

DOCKER_BIN="NO"
DOCKER_SOCKET="NO"
DOCKER_DAEMON="NO"
DOCKER_CONTEXT="UNKNOWN"
DOCKER_HOST_ENV=""
DOCKER_GROUP="NO"
USER_NAME="$(id -un)"

command -v docker >/dev/null 2>&1 && DOCKER_BIN="YES"

[ -S /var/run/docker.sock ] && DOCKER_SOCKET="YES"

DOCKER_HOST_ENV="${DOCKER_HOST:-}"

docker context show >/tmp/delbot_ctx 2>/dev/null || true
[ -f /tmp/delbot_ctx ] && DOCKER_CONTEXT="$(cat /tmp/delbot_ctx)"

id -nG "$USER_NAME" 2>/dev/null | grep -qw docker && DOCKER_GROUP="YES"

docker info >/dev/null 2>&1 && DOCKER_DAEMON="YES"

python3 <<PY
import json

result = {
    "docker_binary": "$DOCKER_BIN",
    "docker_socket": "$DOCKER_SOCKET",
    "docker_daemon": "$DOCKER_DAEMON",
    "docker_context": "$DOCKER_CONTEXT",
    "docker_host_env": "$DOCKER_HOST_ENV",
    "user": "$USER_NAME",
    "docker_group": "$DOCKER_GROUP"
}

if result["docker_daemon"] == "YES":
    result["status"] = "DOCKER_READY"
elif result["docker_socket"] == "NO":
    result["status"] = "SOCKET_NOT_FOUND"
elif result["docker_group"] == "NO":
    result["status"] = "USER_NOT_IN_DOCKER_GROUP"
else:
    result["status"] = "HOST_DOCKER_DAEMON_DOWN"

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
echo "DOCKER_READY -> PR-5.6.2"
echo "HOST_DOCKER_DAEMON_DOWN -> perbaiki host"
echo "USER_NOT_IN_DOCKER_GROUP -> tambah user ke group docker"
echo "SOCKET_NOT_FOUND -> install/start docker"

