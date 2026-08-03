#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BF
#
# vLLM Runtime Probe
#
# MVP SAFE
# ==============================================================================
#
# Tujuan:
#
# Check:
# - vLLM endpoint
# - OpenAI compatible models endpoint
# - Runtime availability
#
# Rules:
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak exit
# - Tidak return
#

set +e

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/vllm_runtime_probe.json"

mkdir -p "$(dirname "$OUTPUT")"


echo "======================================================================"
echo "PR-5.1BF"
echo "vLLM Runtime Probe"
echo "======================================================================"


python3 <<'PY'
import json
import os
import urllib.request
from datetime import datetime


endpoint = os.getenv(
    "OPENAI_API_BASE",
    "http://localhost:8000/v1"
)

result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BF",
    "endpoint": endpoint,
    "runtime": {
        "reachable": False,
        "models_endpoint": False,
        "models": []
    },
    "status": "WAITING_VLLM_RUNTIME"
}


try:
    url = endpoint.rstrip("/") + "/models"

    with urllib.request.urlopen(
        url,
        timeout=3
    ) as response:

        data = json.loads(
            response.read().decode()
        )

        result["runtime"]["reachable"] = True
        result["runtime"]["models_endpoint"] = True

        models = []

        for item in data.get("data", []):
            models.append(
                item.get("id")
            )

        result["runtime"]["models"] = models

        if models:
            result["status"] = "READY_VLLM_RUNTIME"


except Exception as error:
    result["error"] = str(error)


output = "/workspace/delbot/repository_data/mapping/vllm_runtime_probe.json"

with open(output, "w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"


python3 -m compileall \
/workspace/delbot/delbot_platform \
/workspace/delbot/tools \
|| true


echo ""
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo ""
echo "======================================================================"
echo "PR-5.1BF COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "READY_VLLM_RUNTIME -> lanjut PR-5.1BG API Answer Flow"
echo "WAITING_VLLM_RUNTIME -> jalankan vLLM server"

