#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.24
#
# Runtime Gate
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/runtime_gate.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.24 Runtime Gate"
echo "======================================================================"

DOCKER_BINARY=false
DOCKER_SOCKET=false
DOCKER_DAEMON=false
QDRANT_PORT=false
STATUS="HOST_RUNTIME_REQUIRED"

command -v docker >/dev/null 2>&1 && DOCKER_BINARY=true

[ -S /var/run/docker.sock ] && DOCKER_SOCKET=true

if docker info >/dev/null 2>&1; then
    DOCKER_DAEMON=true
fi

if timeout 1 bash -c "</dev/tcp/127.0.0.1/6333" >/dev/null 2>&1; then
    QDRANT_PORT=true
fi

if [ "$DOCKER_DAEMON" = true ]; then
    STATUS="DOCKER_READY"
fi

if [ "$DOCKER_DAEMON" = true ] && [ "$QDRANT_PORT" = true ]; then
    STATUS="QDRANT_READY"
fi

cat > "$OUTPUT" <<EOF
{
  "docker_binary": $DOCKER_BINARY,
  "docker_socket": $DOCKER_SOCKET,
  "docker_daemon": $DOCKER_DAEMON,
  "qdrant_port_6333": $QDRANT_PORT,
  "status": "$STATUS"
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
echo "QDRANT_READY -> PR-5.6.2"
echo "DOCKER_READY -> Start Qdrant Container"
echo "HOST_RUNTIME_REQUIRED -> Fix Docker Host"

