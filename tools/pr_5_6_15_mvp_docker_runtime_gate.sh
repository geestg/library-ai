#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.15
#
# Docker Runtime Gate
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate Docker daemon & Qdrant before continuing embedding.
#
# Tidak:
# - delete
# - restart
# - recreate
# - migration
# - cleanup
# - rebuild
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_runtime_gate.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.15 Docker Runtime Gate"
echo "======================================================================"

python3 <<'PY'
import json
import os
import socket
import subprocess
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=8
        )
        return (
            r.returncode == 0,
            r.stdout.strip(),
            r.stderr.strip()
        )
    except Exception as e:
        return False, "", str(e)

docker_cli = os.path.exists("/usr/bin/docker") or os.path.exists("/bin/docker")
socket_exists = os.path.exists("/var/run/docker.sock")

docker_info_ok, _, docker_info_err = run(["docker", "info"])

qdrant_port = False
try:
    s = socket.create_connection(("127.0.0.1", 6333), timeout=2)
    s.close()
    qdrant_port = True
except Exception:
    pass

if docker_info_ok and qdrant_port:
    status = "READY"
    next_step = "RUN_PR_5_6_2"
elif docker_info_ok:
    status = "START_QDRANT"
    next_step = "START_QDRANT_CONTAINER"
else:
    status = "FIX_DOCKER"
    next_step = "FIX_HOST_RUNTIME"

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_cli": docker_cli,
    "docker_socket": socket_exists,
    "docker_daemon": docker_info_ok,
    "qdrant_port_6333": qdrant_port,
    "status": status,
    "next": next_step
}

with open("/workspace/delbot/repository_data/mapping/docker_runtime_gate.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.15 COMPLETE"

echo
echo "Terminal remains open"
