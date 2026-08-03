#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.20
#
# Docker Daemon Start
#
# SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_daemon_start.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.20 Docker Daemon Start"
echo "======================================================================"

python3 <<'PY'
import json
import os
import socket
import subprocess
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "docker_binary": False,
    "docker_socket": False,
    "docker_daemon_before": False,
    "docker_daemon_after": False,
    "start_attempts": [],
    "status": "UNKNOWN"
}

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        return {
            "ok": r.returncode == 0,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip()
        }
    except Exception as e:
        return {
            "ok": False,
            "stdout": "",
            "stderr": str(e)
        }

result["docker_binary"] = run(["bash","-lc","command -v docker"])["ok"]

sock="/var/run/docker.sock"
result["docker_socket"]=os.path.exists(sock)

before=run(["docker","info"])
result["docker_daemon_before"]=before["ok"]

if not before["ok"]:

    cmds=[
        ["sudo","systemctl","start","docker"],
        ["sudo","service","docker","start"]
    ]

    for cmd in cmds:
        r=run(cmd)
        result["start_attempts"].append({
            "command":" ".join(cmd),
            "success":r["ok"]
        })

        check=run(["docker","info"])
        if check["ok"]:
            break

after=run(["docker","info"])
result["docker_daemon_after"]=after["ok"]

if result["docker_daemon_after"]:
    status="DOCKER_READY"
elif result["docker_socket"]:
    status="HOST_RUNTIME_REQUIRED"
else:
    status="DOCKER_NOT_AVAILABLE"

result["status"]=status

with open("/workspace/delbot/repository_data/mapping/docker_daemon_start.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps({
    "status":result["status"],
    "docker_before":result["docker_daemon_before"],
    "docker_after":result["docker_daemon_after"],
    "attempts":len(result["start_attempts"]),
    "output":"/workspace/delbot/repository_data/mapping/docker_daemon_start.json"
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.20 COMPLETE"

echo
echo "NEXT"
echo "DOCKER_READY -> PR-5.6.21 Qdrant Start"
echo "HOST_RUNTIME_REQUIRED -> Docker dijalankan dari host"
echo
echo "Terminal remains open"

