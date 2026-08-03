#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.7
#
# Qdrant Environment Check
#
# MVP SAFE
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/qdrant_environment_check.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.7 Qdrant Environment Check"
echo "======================================================================"

python3 <<'PY'
import json
import os
import socket
import shutil
from datetime import datetime


result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_binary": False,
    "docker_socket": False,
    "qdrant_port": False,
    "recommendation": ""
}


result["docker_binary"] = shutil.which("docker") is not None

result["docker_socket"] = os.path.exists(
    "/var/run/docker.sock"
)


try:
    s = socket.create_connection(
        ("127.0.0.1",6333),
        timeout=2
    )
    s.close()
    result["qdrant_port"] = True
except:
    result["qdrant_port"] = False


if result["qdrant_port"]:
    result["recommendation"] = "QDRANT_READY"
elif not result["docker_socket"]:
    result["recommendation"] = "DOCKER_RUNTIME_REQUIRED"
else:
    result["recommendation"] = "START_QDRANT_CONTAINER"


with open(
    "/workspace/delbot/repository_data/mapping/qdrant_environment_check.json",
    "w"
) as f:
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
echo "QDRANT_READY -> run PR-5.6.2"
echo "DOCKER_RUNTIME_REQUIRED -> enable docker runtime"
echo "START_QDRANT_CONTAINER -> start qdrant"

echo
echo "Terminal tetap terbuka"
