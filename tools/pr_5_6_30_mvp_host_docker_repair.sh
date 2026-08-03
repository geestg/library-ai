#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.30
#
# Host Docker Repair
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_docker_repair.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.30 Host Docker Repair"
echo "======================================================================"

DOCKER_BIN=false
SOCKET=false
DAEMON=false
GROUP_MEMBER=false
QDRANT=false

command -v docker >/dev/null 2>&1 && DOCKER_BIN=true

[ -S /var/run/docker.sock ] && SOCKET=true

id -nG 2>/dev/null | tr ' ' '\n' | grep -qx docker
[ $? -eq 0 ] && GROUP_MEMBER=true

docker info >/dev/null 2>&1
[ $? -eq 0 ] && DAEMON=true

if [ "$DAEMON" = true ]; then

    docker ps --format '{{.Names}}' 2>/dev/null | grep -qx delbot-qdrant
    [ $? -eq 0 ] && QDRANT=true

fi

ACTION="FIX_HOST_DOCKER"

if [ "$GROUP_MEMBER" = false ]; then
    sudo usermod -aG docker "$USER" >/dev/null 2>&1
    ACTION="LOGIN_AGAIN"
fi

if [ "$DAEMON" = true ] && [ "$QDRANT" = false ]; then
    docker start delbot-qdrant >/dev/null 2>&1
    docker ps --format '{{.Names}}' 2>/dev/null | grep -qx delbot-qdrant
    [ $? -eq 0 ] && QDRANT=true
fi

STATUS="HOST_RUNTIME_REQUIRED"

if [ "$DAEMON" = true ]; then
    STATUS="DOCKER_READY"
fi

if [ "$DAEMON" = true ] && [ "$QDRANT" = true ]; then
    STATUS="QDRANT_READY"
fi

cat > "$OUTPUT" <<EOF
{
  "docker_binary": $DOCKER_BIN,
  "docker_socket": $SOCKET,
  "docker_daemon": $DAEMON,
  "docker_group": $GROUP_MEMBER,
  "qdrant_running": $QDRANT,
  "status": "$STATUS",
  "next_action": "$ACTION"
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
echo "QDRANT_READY -> Jalankan PR-5.6.2"
echo "DOCKER_READY -> docker start delbot-qdrant"
echo "LOGIN_AGAIN -> logout/login atau newgrp docker"
echo "HOST_RUNTIME_REQUIRED -> hidupkan Docker Engine pada host"

