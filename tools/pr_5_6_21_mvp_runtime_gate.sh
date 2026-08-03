#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.21
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
echo "PR-5.6.21 Runtime Gate"
echo "======================================================================"

python3 <<'PY'
import json
import socket
import shutil
import subprocess
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return r.returncode == 0
    except Exception:
        return False

docker_cli = shutil.which("docker") is not None

docker_daemon = False

if docker_cli:
    docker_daemon = run(["docker","info"])

sock = socket.socket()

sock.settimeout(1)

try:
    sock.connect(("127.0.0.1",6333))
    qdrant=True
except Exception:
    qdrant=False

sock.close()

if docker_daemon and qdrant:
    status="READY"
elif docker_daemon:
    status="START_QDRANT"
else:
    status="FIX_HOST_RUNTIME"

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "docker_cli":docker_cli,
    "docker_daemon":docker_daemon,
    "qdrant_port_6333":qdrant,
    "status":status
}

with open("/workspace/delbot/repository_data/mapping/runtime_gate.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.6.21 COMPLETE"

echo

echo "NEXT"
echo "READY -> ulang PR-5.6.2"
echo "START_QDRANT -> jalankan container"
echo "FIX_HOST_RUNTIME -> perbaiki Docker host"

echo
echo "Terminal remains open"

