#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.19
#
# Runtime Preflight
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/runtime_preflight.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.19 Runtime Preflight"
echo "======================================================================"

python3 <<'PY'
import json
import os
import shutil
import socket
import subprocess
from datetime import datetime

def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return {
            "ok": p.returncode == 0,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip()
        }
    except Exception as e:
        return {
            "ok": False,
            "stdout": "",
            "stderr": str(e)
        }

docker_bin = shutil.which("docker") is not None
socket_exists = os.path.exists("/var/run/docker.sock")

docker_info = run(["docker", "info"]) if docker_bin else {
    "ok": False,
    "stdout": "",
    "stderr": "docker binary not found"
}

docker_ps = run(["docker", "ps"]) if docker_bin else {
    "ok": False,
    "stdout": "",
    "stderr": "docker binary not found"
}

qdrant_port = False

try:
    s = socket.create_connection(("127.0.0.1",6333),2)
    qdrant_port = True
    s.close()
except Exception:
    qdrant_port = False

if docker_info["ok"] and qdrant_port:
    status = "READY"
elif docker_info["ok"]:
    status = "START_QDRANT"
elif socket_exists:
    status = "START_DOCKER_DAEMON"
else:
    status = "DOCKER_NOT_INSTALLED"

result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_binary": docker_bin,
    "docker_socket": socket_exists,
    "docker_daemon": docker_info["ok"],
    "docker_ps": docker_ps["ok"],
    "qdrant_port_6333": qdrant_port,
    "status": status
}

with open("/workspace/delbot/repository_data/mapping/runtime_preflight.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.19 COMPLETE"

echo
echo "NEXT"
echo "READY"
echo "START_QDRANT"
echo "START_DOCKER_DAEMON"
echo "DOCKER_NOT_INSTALLED"

echo
echo "Terminal remains open"

