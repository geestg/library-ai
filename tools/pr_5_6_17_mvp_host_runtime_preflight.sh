#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.17
#
# Host Runtime Preflight
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_preflight.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.17 Host Runtime Preflight"
echo "======================================================================"

python3 <<'PY'
import json
import os
import socket
import shutil
import subprocess
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_binary": shutil.which("docker") is not None,
    "docker_socket": os.path.exists("/var/run/docker.sock"),
    "docker_daemon": False,
    "qdrant_port": False,
    "recommendation": ""
}

if result["docker_binary"]:
    try:
        r = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        result["docker_daemon"] = (r.returncode == 0)
    except Exception:
        pass

try:
    s = socket.create_connection(("127.0.0.1", 6333), timeout=2)
    s.close()
    result["qdrant_port"] = True
except Exception:
    pass

if not result["docker_binary"]:
    result["recommendation"] = "INSTALL_DOCKER"
elif not result["docker_daemon"]:
    result["recommendation"] = "START_DOCKER_DAEMON"
elif not result["qdrant_port"]:
    result["recommendation"] = "START_QDRANT"
else:
    result["recommendation"] = "READY_FOR_PR_5_6_2"

with open("/workspace/delbot/repository_data/mapping/host_runtime_preflight.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.17 COMPLETE"
echo
echo "NEXT"
echo "READY_FOR_PR_5_6_2"
echo "START_QDRANT"
echo "START_DOCKER_DAEMON"

