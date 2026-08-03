#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.37
#
# Host Detection
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

OUTPUT="/workspace/delbot/repository_data/mapping/host_detection.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.37 Host Detection"
echo "======================================================================"

python3 <<PY
import json
import os
import pathlib
import subprocess

def run(cmd):
    try:
        r=subprocess.run(cmd,shell=True,text=True,capture_output=True)
        return (r.returncode,r.stdout.strip(),r.stderr.strip())
    except Exception as e:
        return (1,"",str(e))

def exists(p):
    return pathlib.Path(p).exists()

data={}

data["hostname"]=pathlib.Path("/etc/hostname").read_text().strip() if exists("/etc/hostname") else ""

data["inside_docker"]=exists("/.dockerenv")

data["pid1"]=(pathlib.Path("/proc/1/comm").read_text().strip()
             if exists("/proc/1/comm") else "")

rc,out,err=run("systemd-detect-virt")

data["virtualization"]=out if rc==0 else ""

rc,out,err=run("cat /proc/self/cgroup")

data["cgroup"]=out.splitlines()[:5]

rc,out,err=run("docker info")

data["docker_daemon"]=(rc==0)

rc,out,err=run("id -nG")

data["groups"]=out

status="UNKNOWN"

if data["inside_docker"]:
    status="RUNNING_INSIDE_DOCKER_CONTAINER"

elif data["virtualization"]=="docker":
    status="RUNNING_INSIDE_DOCKER_CONTAINER"

elif data["docker_daemon"]:
    status="HOST_READY"

else:
    status="HOST_WITHOUT_DOCKER"

data["status"]=status

with open("$OUTPUT","w") as f:
    json.dump(data,f,indent=2)

print(json.dumps({
    "inside_docker":data["inside_docker"],
    "pid1":data["pid1"],
    "virtualization":data["virtualization"],
    "docker_daemon":data["docker_daemon"],
    "status":status
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "HOST_READY"
echo "RUNNING_INSIDE_DOCKER_CONTAINER"
echo "HOST_WITHOUT_DOCKER"

