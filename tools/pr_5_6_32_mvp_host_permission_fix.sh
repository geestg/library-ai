#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.32
#
# Host Permission Fix
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_permission_fix.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.32 Host Permission Fix"
echo "======================================================================"

USER_NAME="$(id -un)"

DOCKER_GROUP=false
DOCKER_DAEMON=false
DOCKER_SOCKET=false

[ -S /var/run/docker.sock ] && DOCKER_SOCKET=true

id -nG "$USER_NAME" 2>/dev/null | grep -qw docker
[ $? -eq 0 ] && DOCKER_GROUP=true

docker info >/dev/null 2>&1
[ $? -eq 0 ] && DOCKER_DAEMON=true

if [ "$DOCKER_GROUP" = false ]; then
    sudo usermod -aG docker "$USER_NAME" >/dev/null 2>&1
fi

cat > "$OUTPUT" <<EOF
{
  "docker_socket": $DOCKER_SOCKET,
  "docker_group": $DOCKER_GROUP,
  "docker_daemon": $DOCKER_DAEMON,
  "user": "$USER_NAME",
  "status": "$(
    if [ "$DOCKER_DAEMON" = true ]; then
        echo READY
    elif [ "$DOCKER_GROUP" = false ]; then
        echo LOGIN_REQUIRED
    else
        echo START_DOCKER_DAEMON
    fi
  )"
}
EOF

cat "$OUTPUT"

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "READY"
echo "LOGIN_REQUIRED"
echo "START_DOCKER_DAEMON"

