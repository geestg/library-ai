#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.3
#
# Qdrant Service Repair Check
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate Qdrant runtime before embedding indexing
#
# Tidak melakukan:
# - delete volume
# - delete collection
# - migration
# - cleanup data
# - exit
# - return
#
# Terminal tetap terbuka
#

set -u

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.3 Qdrant Service Repair Check"
echo "======================================================================"

OUTPUT="/workspace/delbot/repository_data/mapping/qdrant_service_check.json"

mkdir -p "$(dirname "$OUTPUT")"

python3 <<'PY'
import json
import subprocess
import urllib.request
from datetime import datetime

container = "delbot-qdrant"

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "container": container,
    "docker_exists": False,
    "container_running": False,
    "health_endpoint": False,
    "action": "NONE"
}


try:
    containers = subprocess.check_output(
        [
            "docker",
            "ps",
            "-a",
            "--format",
            "{{.Names}}"
        ],
        text=True
    ).splitlines()

    if container in containers:
        result["docker_exists"] = True

except Exception:
    pass


if result["docker_exists"]:

    try:
        running = subprocess.check_output(
            [
                "docker",
                "inspect",
                "-f",
                "{{.State.Running}}",
                container
            ],
            text=True
        ).strip()

        if running == "true":
            result["container_running"] = True

    except Exception:
        pass


if not result["container_running"]:

    try:
        subprocess.run(
            [
                "docker",
                "start",
                container
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        result["action"] = "START_CONTAINER"

    except Exception:
        result["action"] = "START_FAILED"


try:

    response = urllib.request.urlopen(
        "http://localhost:6333/healthz",
        timeout=5
    )

    if response.status == 200:
        result["health_endpoint"] = True

except Exception:
    pass


if result["health_endpoint"]:
    result["status"] = "QDRANT_READY"
else:
    result["status"] = "QDRANT_NOT_READY"


with open(
    "/workspace/delbot/repository_data/mapping/qdrant_service_check.json",
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "QDRANT_READY -> run PR-5.6.2 again"
echo "QDRANT_NOT_READY -> inspect docker logs"

echo
echo "Terminal remains open"

