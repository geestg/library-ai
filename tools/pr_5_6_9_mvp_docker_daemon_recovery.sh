#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.9
#
# Docker Daemon Recovery Check
#
# SAFE
#
# Tidak:
# - delete
# - recreate container
# - remove volume
# - migration
# - cleanup
#
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_daemon_recovery.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.9 Docker Daemon Recovery"
echo "======================================================================"

python3 <<'PY'
import json
import subprocess
import shutil
from datetime import datetime


def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "ok": p.returncode == 0,
            "stdout": p.stdout[-500:],
            "stderr": p.stderr[-500:]
        }
    except Exception as e:
        return {
            "ok": False,
            "stdout": "",
            "stderr": str(e)
        }


result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_binary": bool(shutil.which("docker")),
    "before": {},
    "actions": [],
    "after": {},
    "status": ""
}


result["before"] = run("docker info")


if not result["before"]["ok"]:

    services = [
        "sudo service docker start",
        "sudo systemctl start docker"
    ]

    for cmd in services:
        r = run(cmd)

        result["actions"].append({
            "command": cmd,
            "success": r["ok"]
        })

        if r["ok"]:
            break


result["after"] = run("docker info")


if result["after"]["ok"]:
    result["status"] = "DOCKER_READY"
else:
    result["status"] = "DOCKER_DAEMON_UNAVAILABLE"


with open(
    "/workspace/delbot/repository_data/mapping/docker_daemon_recovery.json",
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps({
    "status": result["status"],
    "docker_ready": result["after"]["ok"],
    "actions": result["actions"]
}, indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "NEXT"
echo "DOCKER_READY -> run Qdrant startup"
echo "DOCKER_DAEMON_UNAVAILABLE -> Docker host runtime issue"

echo

echo "Terminal tetap terbuka"
