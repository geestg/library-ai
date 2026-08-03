#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.35
#
# Runtime Environment Probe
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

OUTPUT="/workspace/delbot/repository_data/mapping/runtime_environment_probe.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.35 Runtime Environment Probe"
echo "======================================================================"

python3 <<PY
import json
import os
import pathlib
import subprocess

def run(cmd):
    try:
        r = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return (r.returncode == 0), r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return False, "", str(e)

env = {}

env["hostname"] = pathlib.Path("/etc/hostname").read_text().strip() if pathlib.Path("/etc/hostname").exists() else ""

env["container"] = os.path.exists("/.dockerenv")

ok, out, _ = run("systemd-detect-virt")

env["systemd_detect_virt"] = out if ok else ""

ok, out, _ = run("cat /proc/1/comm")

env["pid1"] = out

ok, out, _ = run("cat /proc/1/cgroup")

env["cgroup"] = out[:300]

ok, out, _ = run("docker version")

env["docker_daemon"] = ok

result = {
    "environment": env,
    "status": (
        "RUNNING_INSIDE_CONTAINER"
        if env["container"]
        else "RUNNING_ON_HOST"
    )
}

with open("$OUTPUT","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "Paste hasil JSON"

