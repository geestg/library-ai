#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.33
#
# Host Runtime Capability Check
#
# SAFE
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# Output ringkas
# ==============================================================================

set +e
set -u

OUTPUT="/workspace/delbot/repository_data/mapping/host_runtime_capability_check.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.33 Host Runtime Capability Check"
echo "======================================================================"

python3 <<PY
import json
import os
import subprocess

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "ok": r.returncode == 0,
        "stdout": r.stdout.strip(),
        "stderr": r.stderr.strip()
    }

result = {}

result["docker_binary"] = os.path.exists("/usr/bin/docker") or os.path.exists("/bin/docker")
result["docker_socket"] = os.path.exists("/var/run/docker.sock")

result["docker_version"] = run("docker version --format '{{.Server.Version}}'")
result["docker_info"] = run("docker info")
result["docker_ps"] = run("docker ps --format '{{.Names}}'")

inside_container = os.path.exists("/.dockerenv")
result["inside_container"] = inside_container

if inside_container:
    try:
        with open("/proc/1/cgroup","r") as f:
            txt=f.read().lower()
        result["container_runtime"] = (
            "docker" if "docker" in txt else
            "containerd" if "containerd" in txt else
            "unknown"
        )
    except Exception:
        result["container_runtime"]="unknown"
else:
    result["container_runtime"]="host"

if result["docker_info"]["ok"]:
    status="DOCKER_READY"
elif result["docker_socket"]:
    status="HOST_DOCKER_UNAVAILABLE"
else:
    status="NO_DOCKER_SOCKET"

result["status"]=status

with open("$OUTPUT","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps({
    "inside_container":result["inside_container"],
    "container_runtime":result["container_runtime"],
    "docker_socket":result["docker_socket"],
    "docker_daemon":result["docker_info"]["ok"],
    "status":result["status"]
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "DOCKER_READY"
echo "HOST_DOCKER_UNAVAILABLE"
echo "NO_DOCKER_SOCKET"

