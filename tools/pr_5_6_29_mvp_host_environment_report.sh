#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.29
#
# Host Environment Report
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_environment_report.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.29 Host Environment Report"
echo "======================================================================"

docker_binary=false
docker_socket=false
docker_daemon=false
docker_group=false
qdrant_port=false

if command -v docker >/dev/null 2>&1; then
    docker_binary=true
fi

if [ -S /var/run/docker.sock ]; then
    docker_socket=true
fi

if docker info >/dev/null 2>&1; then
    docker_daemon=true
fi

if id -nG 2>/dev/null | tr ' ' '\n' | grep -qx docker; then
    docker_group=true
fi

if command -v ss >/dev/null 2>&1; then
    if ss -ltn 2>/dev/null | grep -q ':6333 '; then
        qdrant_port=true
    fi
elif command -v netstat >/dev/null 2>&1; then
    if netstat -ltn 2>/dev/null | grep -q ':6333 '; then
        qdrant_port=true
    fi
fi

STATUS="HOST_RUNTIME_REQUIRED"

if [ "$docker_daemon" = true ]; then
    STATUS="DOCKER_READY"
fi

if [ "$docker_daemon" = true ] && [ "$qdrant_port" = true ]; then
    STATUS="QDRANT_READY"
fi

cat > "$OUTPUT" <<EOF
{
  "docker_binary": $docker_binary,
  "docker_socket": $docker_socket,
  "docker_daemon": $docker_daemon,
  "docker_group": $docker_group,
  "qdrant_port_6333": $qdrant_port,
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
echo "QDRANT_READY -> Run PR-5.6.2"
echo "DOCKER_READY -> Start Qdrant Container"
echo "HOST_RUNTIME_REQUIRED -> Fix Docker Host"

