#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.6
#
# Qdrant Runtime Recovery Check
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# - Recover docker/qdrant runtime
# - Validate Qdrant availability
#
# Tidak melakukan:
# - delete container
# - delete volume
# - delete collection
# - migration
# - rebuild index
#
# Terminal tetap terbuka
#

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/qdrant_runtime_recovery.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.6 Qdrant Runtime Recovery"
echo "======================================================================"


python3 <<'PY'
import json
import subprocess
import socket
import time
from datetime import datetime


output="/workspace/delbot/repository_data/mapping/qdrant_runtime_recovery.json"


def run(cmd):
    try:
        result=subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "ok": result.returncode == 0,
            "out": result.stdout.strip()[-300:],
            "err": result.stderr.strip()[-300:]
        }

    except Exception as e:
        return {
            "ok": False,
            "out": "",
            "err": str(e)
        }


docker_check = run("docker info")


docker_started = False

if not docker_check["ok"]:

    systemctl = run(
        "systemctl start docker"
    )

    time.sleep(3)

    docker_check = run(
        "docker info"
    )

    docker_started = systemctl["ok"]



container_check = run(
    "docker ps -a --format '{{.Names}}' | grep '^delbot-qdrant$'"
)


container_started = False

if docker_check["ok"]:

    if container_check["ok"]:

        start = run(
            "docker start delbot-qdrant"
        )

        container_started = start["ok"]


health = False

try:
    sock = socket.create_connection(
        ("127.0.0.1",6333),
        timeout=3
    )

    sock.close()
    health=True

except:
    health=False



result={

    "timestamp":
        datetime.utcnow().isoformat()+"Z",

    "docker_available":
        docker_check["ok"],

    "docker_started":
        docker_started,

    "qdrant_container_exists":
        container_check["ok"],

    "qdrant_container_started":
        container_started,

    "qdrant_port_6333":
        health,

    "status":
        (
            "QDRANT_READY"
            if health
            else "QDRANT_NOT_READY"
        ),

    "next":
        (
            "RUN_PR_5_6_2"
            if health
            else "CHECK_DOCKER_RUNTIME"
        )
}



with open(output,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result,indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.6 COMPLETE"

echo
echo "NEXT:"
echo "QDRANT_READY -> run PR-5.6.2 embedding retry"
echo "QDRANT_NOT_READY -> inspect docker runtime"

echo
echo "Terminal tetap terbuka"
