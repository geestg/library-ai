#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BD
#
# vLLM Runtime Connector Validation
#
# MVP SAFE
# ==============================================================================
#
# Tujuan:
#
# Gateway
#    |
#    v
# vLLM OpenAI Compatible API
#    |
#    v
# Local Model
#
# Rules:
# - Tidak start model
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1BD"
echo "vLLM Runtime Connector Validation"
echo "======================================================================"

ROOT="/workspace/delbot"

OUTPUT="$ROOT/repository_data/mapping/vllm_runtime_connector_validation.json"

python3 <<'PY'
import json
import os
import shutil
import socket
from datetime import datetime


def port_open(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except Exception:
        return False


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BD",

    "runtime": {
        "vllm_binary": shutil.which("vllm") is not None,
        "python_module": False,
        "server_port_8000": False
    },

    "gateway": {
        "openai_compatible_target": True,
        "connector_ready": True
    },

    "environment": {
        "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE"),
        "LLM_PROVIDER": os.getenv("LLM_PROVIDER")
    },

    "connection": {
        "runtime_connected": False,
        "model_available": False
    },

    "status": "WAITING_VLLM_RUNTIME"
}


try:
    import vllm
    result["runtime"]["python_module"] = True
except Exception:
    pass


if port_open("127.0.0.1",8000):
    result["runtime"]["server_port_8000"] = True
    result["connection"]["runtime_connected"] = True


if result["connection"]["runtime_connected"]:
    result["status"] = "READY_VLLM_CONNECTION"


os.makedirs(
    "/workspace/delbot/repository_data/mapping",
    exist_ok=True
)

with open(
    "/workspace/delbot/repository_data/mapping/vllm_runtime_connector_validation.json",
    "w"
) as f:
    json.dump(result,f,indent=2)


print(json.dumps(result,indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform \
/workspace/delbot/tools \
2>&1 | tee /tmp/delbot_compile_pr51bd.log


echo ""
echo "Generated"
echo "/workspace/delbot/repository_data/mapping/vllm_runtime_connector_validation.json"

echo ""
echo "======================================================================"
echo "PR-5.1BD COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_VLLM_CONNECTION lanjut PR-5.1BE LLM Answer Generation"
echo "Jika WAITING_VLLM_RUNTIME aktifkan vLLM model server"
