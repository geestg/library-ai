#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.8
#
# Docker Runtime Probe
#
# MVP SAFE
#
# Tidak:
# - delete
# - recreate
# - migration
# - cleanup
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_runtime_probe.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.8 Docker Runtime Probe"
echo "======================================================================"

python3 <<'PY'
import json
import subprocess
import os
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
            "stdout": p.stdout.strip()[:200],
            "stderr": p.stderr.strip()[:200]
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


result = {
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "docker_cli": run("docker --version"),
    "docker_info": run("docker info"),
    "socket_exists": os.path.exists("/var/run/docker.sock"),
    "status": "UNKNOWN"
}


if result["docker_info"]["ok"]:
    result["status"] = "DOCKER_READY"

elif result["socket_exists"]:
    result["status"] = "DOCKER_SOCKET_ONLY"

else:
    result["status"] = "DOCKER_UNAVAILABLE"


with open(
    "/workspace/delbot/repository_data/mapping/docker_runtime_probe.json",
    "w"
) as f:
    json.dump(result, f, indent=2)


print(json.dumps({
    "status": result["status"],
    "docker_cli": result["docker_cli"]["ok"],
    "docker_info": result["docker_info"]["ok"],
    "socket": result["socket_exists"]
}, indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.8 COMPLETE"
echo
echo "NEXT:"
echo "DOCKER_READY -> start Qdrant check"
echo "DOCKER_SOCKET_ONLY -> enable docker daemon"
echo "DOCKER_UNAVAILABLE -> inspect runtime"
echo
echo "Terminal tetap terbuka"
