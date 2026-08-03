#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.13
#
# Host Runtime Full Diagnostic
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
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_full_diagnostic.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.13 Host Runtime Full Diagnostic"
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
            timeout=8
        )
        return {
            "ok": p.returncode == 0,
            "stdout": p.stdout.strip()[:400],
            "stderr": p.stderr.strip()[:400]
        }
    except Exception as e:
        return {
            "ok": False,
            "stdout": "",
            "stderr": str(e)
        }

result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_binary": shutil.which("docker") is not None,
    "docker_socket_exists": os.path.exists("/var/run/docker.sock"),
    "docker_socket_connectable": False,
    "docker_info": {},
    "docker_ps": {},
    "systemctl": {},
    "service": {},
    "qdrant_port_6333": False,
    "host_runtime": "",
    "recommended_action": ""
}

if result["docker_socket_exists"]:
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect("/var/run/docker.sock")
        s.close()
        result["docker_socket_connectable"] = True
    except Exception:
        pass

result["docker_info"] = run(["docker","info"])
result["docker_ps"]   = run(["docker","ps"])
result["systemctl"]   = run(["systemctl","status","docker","--no-pager"])
result["service"]     = run(["service","docker","status"])

try:
    s = socket.create_connection(("127.0.0.1",6333),2)
    s.close()
    result["qdrant_port_6333"]=True
except Exception:
    pass

if result["docker_info"]["ok"]:
    result["host_runtime"]="DOCKER_READY"
    if result["qdrant_port_6333"]:
        result["recommended_action"]="RUN_PR_5_6_2"
    else:
        result["recommended_action"]="START_QDRANT"
else:
    if result["docker_socket_exists"]:
        result["host_runtime"]="DOCKER_DAEMON_DOWN"
        result["recommended_action"]="FIX_DOCKER_HOST"
    else:
        result["host_runtime"]="DOCKER_NOT_INSTALLED"
        result["recommended_action"]="INSTALL_DOCKER"

with open("/workspace/delbot/repository_data/mapping/host_runtime_full_diagnostic.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps({
    "status":result["host_runtime"],
    "recommendation":result["recommended_action"],
    "docker_info":result["docker_info"]["ok"],
    "docker_ps":result["docker_ps"]["ok"],
    "socket":result["docker_socket_exists"],
    "socket_connectable":result["docker_socket_connectable"],
    "qdrant_port":result["qdrant_port_6333"],
    "output":"/workspace/delbot/repository_data/mapping/host_runtime_full_diagnostic.json"
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.13 COMPLETE"

echo
echo "NEXT"
echo "DOCKER_READY -> PR-5.6.2"
echo "FIX_DOCKER_HOST -> repair docker daemon"

echo
echo "Terminal remains open"
