#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.38
#
# Docker API Probe
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_api_probe.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.38 Docker API Probe"
echo "======================================================================"

SOCKET_EXISTS=false
SOCKET_ACCESS=false
DOCKER_API=false

[ -S /var/run/docker.sock ] && SOCKET_EXISTS=true
[ -r /var/run/docker.sock ] && [ -w /var/run/docker.sock ] && SOCKET_ACCESS=true

HTTP_CODE=""

if command -v curl >/dev/null 2>&1; then
    HTTP_CODE=$(curl \
        --silent \
        --show-error \
        --unix-socket /var/run/docker.sock \
        http://localhost/_ping \
        2>/dev/null)
fi

if [ "$HTTP_CODE" = "OK" ]; then
    DOCKER_API=true
fi

cat > "$OUTPUT" <<EOF
{
  "socket_exists": $SOCKET_EXISTS,
  "socket_access": $SOCKET_ACCESS,
  "docker_api": $DOCKER_API,
  "status": "$(
if [ "$DOCKER_API" = true ]; then
    echo READY
else
    echo HOST_DOCKER_NOT_EXPOSED
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
echo "READY -> ulang PR-5.6.2"
echo "HOST_DOCKER_NOT_EXPOSED -> perbaiki container runtime"

