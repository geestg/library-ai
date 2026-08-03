#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.22
#
# Host Runtime Final Check
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_final_check.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.22 Host Runtime Final Check"
echo "======================================================================"

python3 <<'PY'
import json
import subprocess
import socket
import shutil
import os
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=8
        )
        return {
            "ok": r.returncode == 0,
            "stdout": r.stdout.strip()[:300],
            "stderr": r.stderr.strip()[:300]
        }
    except Exception as e:
        return {
            "ok": False,
            "stdout": "",
            "stderr": str(e)
        }

def port_open(port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_binary": shutil.which("docker") is not None,
    "docker_socket": os.path.exists("/var/run/docker.sock"),
    "docker_version": run(["docker","version"]),
    "docker_info": run(["docker","info"]),
    "docker_ps": run(["docker","ps"]),
    "systemctl": run(["systemctl","status","docker"]),
    "service": run(["service","docker","status"]),
    "qdrant_port": port_open(6333)
}

if result["docker_info"]["ok"]:
    status="DOCKER_READY"
elif result["docker_socket"]:
    status="DOCKER_DAEMON_DOWN"
else:
    status="DOCKER_NOT_INSTALLED"

result["status"]=status

with open(OUTPUT,"w") as f:
    json.dump(result,f,indent=2)

print(json.dumps({
    "status":status,
    "docker_binary":result["docker_binary"],
    "docker_socket":result["docker_socket"],
    "docker_info":result["docker_info"]["ok"],
    "docker_ps":result["docker_ps"]["ok"],
    "qdrant_port":result["qdrant_port"],
    "output":OUTPUT
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.22 COMPLETE"

echo
echo "NEXT"
echo "DOCKER_READY -> PR-5.6.2"
echo "DOCKER_DAEMON_DOWN -> FIX HOST"
echo "DOCKER_NOT_INSTALLED -> INSTALL HOST"

echo
echo "Terminal remains open"

