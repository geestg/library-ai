#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.11
#
# Docker Host Validation
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
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_host_validation.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.11 Docker Host Validation"
echo "======================================================================"

python3 <<'PY'
import json
import os
import socket
import subprocess
import datetime

result = {
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
}

result["docker_binary"] = os.path.exists("/usr/bin/docker") or os.path.exists("/bin/docker")
result["docker_socket_exists"] = os.path.exists("/var/run/docker.sock")

try:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(1)
    s.connect("/var/run/docker.sock")
    s.close()
    result["socket_connectable"] = True
except Exception:
    result["socket_connectable"] = False

try:
    r = subprocess.run(
        ["docker", "version", "--format", "{{.Server.Version}}"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    result["docker_server_available"] = (r.returncode == 0)

    if r.returncode == 0:
        result["server_version"] = r.stdout.strip()
    else:
        err = (r.stderr or "").strip()
        if len(err) > 200:
            err = err[:200]
        result["error"] = err

except Exception as e:
    result["docker_server_available"] = False
    result["error"] = str(e)

if result["docker_server_available"]:
    result["status"] = "DOCKER_READY"
elif result["socket_connectable"]:
    result["status"] = "DOCKER_DAEMON_NOT_RESPONDING"
elif result["docker_socket_exists"]:
    result["status"] = "SOCKET_EXISTS_BUT_UNREACHABLE"
else:
    result["status"] = "DOCKER_NOT_INSTALLED_OR_SOCKET_MISSING"

with open("/workspace/delbot/repository_data/mapping/docker_host_validation.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.11 COMPLETE"

echo
echo "NEXT"
echo "DOCKER_READY -> PR-5.6.2"
echo "OTHER_STATUS -> fix host runtime"

echo
echo "Terminal remains open"

