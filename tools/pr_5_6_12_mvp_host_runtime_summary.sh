#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.12
#
# Host Runtime Summary
#
# SAFE
#
# Tidak:
# - delete
# - restart
# - recreate
# - migration
# - cleanup
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_summary.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.12 Host Runtime Summary"
echo "======================================================================"

python3 <<'PY'
import json
import os
import shutil
import socket
import subprocess
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_binary": shutil.which("docker") is not None,
    "docker_socket_exists": os.path.exists("/var/run/docker.sock"),
    "docker_info": False,
    "docker_error": "",
    "qdrant_port_6333": False,
    "host_runtime": "UNKNOWN",
    "next_action": ""
}

try:
    r = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10
    )
    if r.returncode == 0:
        result["docker_info"] = True
    else:
        result["docker_error"] = r.stderr.strip()
except Exception as e:
    result["docker_error"] = str(e)

try:
    s = socket.create_connection(("127.0.0.1", 6333), timeout=2)
    s.close()
    result["qdrant_port_6333"] = True
except Exception:
    pass

if not result["docker_binary"]:
    result["host_runtime"] = "DOCKER_NOT_INSTALLED"
    result["next_action"] = "INSTALL_DOCKER"

elif not result["docker_socket_exists"]:
    result["host_runtime"] = "DOCKER_SOCKET_MISSING"
    result["next_action"] = "START_DOCKER_HOST"

elif not result["docker_info"]:
    result["host_runtime"] = "DOCKER_DAEMON_UNAVAILABLE"
    result["next_action"] = "FIX_HOST_DOCKER"

elif not result["qdrant_port_6333"]:
    result["host_runtime"] = "START_QDRANT"

else:
    result["host_runtime"] = "READY"
    result["next_action"] = "RUN_PR_5_6_2"

with open("/workspace/delbot/repository_data/mapping/host_runtime_summary.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.12 COMPLETE"
echo
echo "Terminal remains open"

