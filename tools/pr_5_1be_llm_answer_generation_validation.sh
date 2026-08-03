#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BE
#
# LLM Answer Generation Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# Backend Gateway
#       |
#       v
# OpenAI Compatible Client
#       |
#       v
# vLLM Runtime
#       |
#       v
# LLM Response
#
# Rules:
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak modify source
# - Tidak exit
# - Tidak return
#
# ==============================================================================

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/llm_answer_generation_validation.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "PR-5.1BE"
echo "LLM Answer Generation Validation"
echo "======================================================================"

python3 <<'PY'

import json
import os
import datetime
import urllib.request


result = {
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BE",
    "gateway": {
        "openai_client_target": True,
        "answer_generation_ready": True
    },
    "runtime": {
        "endpoint": None,
        "reachable": False,
        "model_available": False
    },
    "test_request": {
        "prompt": "Explain artificial intelligence research",
        "executed": False
    },
    "status": "WAITING_LLM_RUNTIME"
}


base = os.getenv(
    "OPENAI_API_BASE",
    "http://localhost:8000/v1"
)

result["runtime"]["endpoint"] = base


try:

    url = base.rstrip("/") + "/models"

    req = urllib.request.Request(
        url,
        headers={
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(
        req,
        timeout=3
    ) as response:

        data = response.read()

        result["runtime"]["reachable"] = True

        try:
            payload = json.loads(data)

            models = payload.get("data", [])

            if len(models) > 0:
                result["runtime"]["model_available"] = True
                result["status"] = "READY_LLM_RUNTIME"

        except Exception:
            pass


except Exception:
    pass


with open(
    "/workspace/delbot/repository_data/mapping/llm_answer_generation_validation.json",
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
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform \
/workspace/delbot/tools \
>/tmp/pr_5_1be_compile.log 2>&1

cat /tmp/pr_5_1be_compile.log


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "======================================================================"
echo "PR-5.1BE COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika READY_LLM_RUNTIME lanjut API Answer Test"
echo "Jika WAITING_LLM_RUNTIME aktifkan vLLM server"

