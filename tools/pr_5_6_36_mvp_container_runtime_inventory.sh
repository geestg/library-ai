#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.36
#
# Container Runtime Inventory
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

OUTPUT="/workspace/delbot/repository_data/mapping/container_runtime_inventory.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.36 Container Runtime Inventory"
echo "======================================================================"

python3 <<PY
import json
import os
import pathlib
import shutil
import socket
import subprocess

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "code": r.returncode,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip()
        }
    except Exception as e:
        return {
            "code": -1,
            "stdout": "",
            "stderr": str(e)
        }

data = {}

data["hostname"] = socket.gethostname()
data["user"] = run("whoami")["stdout"]
data["pwd"] = os.getcwd()

data["inside_container"] = pathlib.Path("/.dockerenv").exists()

data["pid1"] = run("ps -p 1 -o comm=")["stdout"]

data["docker_binary"] = shutil.which("docker") is not None

sock="/var/run/docker.sock"

data["docker_socket_exists"]=os.path.exists(sock)

data["docker_socket_access"]=os.access(sock,os.R_OK|os.W_OK)

info=run("docker info")

data["docker_daemon"]=info["code"]==0

ctx=run("docker context show")

data["docker_context"]=ctx["stdout"]

data["groups"]=run("groups")["stdout"]

port=False

try:
    s=socket.create_connection(("127.0.0.1",6333),1)
    s.close()
    port=True
except:
    pass

data["qdrant_port_6333"]=port

if data["inside_container"] and not data["docker_daemon"]:
    status="CONTAINER_WITHOUT_HOST_DOCKER"
elif data["docker_daemon"] and not port:
    status="START_QDRANT"
elif data["docker_daemon"] and port:
    status="READY_FOR_PR_5_6_2"
else:
    status="UNKNOWN"

data["status"]=status

with open("$OUTPUT","w") as f:
    json.dump(data,f,indent=2)

print(json.dumps(data,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "READY_FOR_PR_5_6_2"
echo "START_QDRANT"
echo "CONTAINER_WITHOUT_HOST_DOCKER"

