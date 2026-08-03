#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.31
#
# Docker Group Repair
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_group_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.31 Docker Group Repair"
echo "======================================================================"

USER_NAME="$(id -un)"

GROUP_EXISTS=false
USER_IN_GROUP=false

getent group docker >/dev/null 2>&1
if [ $? -eq 0 ]; then
    GROUP_EXISTS=true
fi

id -nG "$USER_NAME" | tr ' ' '\n' | grep -qx docker
if [ $? -eq 0 ]; then
    USER_IN_GROUP=true
else
    if [ "$GROUP_EXISTS" = true ]; then
        sudo usermod -aG docker "$USER_NAME" >/dev/null 2>&1 || true
        id -nG "$USER_NAME" | tr ' ' '\n' | grep -qx docker
        if [ $? -eq 0 ]; then
            USER_IN_GROUP=true
        fi
    fi
fi

python3 <<PY
import json

result={
    "docker_group_exists": ${GROUP_EXISTS},
    "user":"${USER_NAME}",
    "user_in_docker_group": ${USER_IN_GROUP},
    "next":"LOGIN_AGAIN" if not ${USER_IN_GROUP} else "CHECK_DOCKER_DAEMON"
}

with open("${OUTPUT}","w") as f:
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
echo "LOGIN_AGAIN"
echo "atau"
echo "CHECK_DOCKER_DAEMON"

