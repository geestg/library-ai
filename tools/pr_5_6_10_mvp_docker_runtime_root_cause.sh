#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.6.10
#
# Docker Runtime Root Cause
#
# SAFE
#
# Tidak:
# - delete
# - recreate
# - restart
# - migration
# - cleanup
#
# Tidak ada exit
# Tidak ada return
# Terminal tetap terbuka
# ==============================================================================

set -u

OUTPUT="/workspace/delbot/repository_data/mapping/docker_runtime_root_cause.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.6.10 Docker Runtime Root Cause"
echo "======================================================================"

python3 <<'PY'
import json
import os
import shutil
import socket
import subprocess
from datetime import datetime

result = {
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

result["docker_binary"] = shutil.which("docker") is not None

sock = "/var/run/docker.sock"
result["docker_socket"] = os.path.exists(sock)

try:
    st = os.stat(sock)
    result["socket_uid"] = st.st_uid
    result["socket_gid"] = st.st_gid
    result["socket_mode"] = oct(st.st_mode & 0o777)
except Exception:
    pass

try:
    s = socket.create_connection(("127.0.0.1", 6333), timeout=1)
    s.close()
    result["qdrant_port"] = True
except Exception:
    result["qdrant_port"] = False

try:
    p = subprocess.run(
        ["docker","info"],
        capture_output=True,
        text=True,
        timeout=10
    )
    result["docker_info_ok"] = (p.returncode == 0)
    result["docker_info_error"] = (
        p.stderr.strip().splitlines()[-1]
        if p.stderr.strip()
        else ""
    )
except Exception as e:
    result["docker_info_ok"] = False
    result["docker_info_error"] = str(e)

if result["docker_info_ok"]:
    status = "DOCKER_READY"
elif result["docker_socket"]:
    status = "DOCKER_DAEMON_NOT_RUNNING_OR_PERMISSION"
else:
    status = "DOCKER_NOT_INSTALLED"

result["status"] = status

with open("/workspace/delbot/repository_data/mapping/docker_runtime_root_cause.json","w") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "PR-5.6.10 COMPLETE"
echo
echo "NEXT"
echo "DOCKER_READY -> PR-5.6.2"
echo "DAEMON_NOT_RUNNING -> repair docker host"
echo "PERMISSION -> add docker group"
echo
echo "Terminal remains open"

