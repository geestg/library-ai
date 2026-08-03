#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BH
#
# Chat Endpoint Test Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# Client Request
#       |
#       v
# Backend API
#       |
#       v
# Gateway
#       |
#       v
# LLM Connector
#
# Rules:
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak exit
# - Tidak return
#
# ==============================================================================

set +e

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/chat_endpoint_test_validation.json"

mkdir -p "$(dirname "$OUTPUT")"

python3 <<'PY'
import json
import os
import urllib.request
import urllib.error
from datetime import datetime


root = "/workspace/delbot"

result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BH",
    "endpoint": {
        "path": "/chat",
        "tested": False,
        "reachable": False
    },
    "request": {
        "prompt": "Explain artificial intelligence research",
        "sent": False
    },
    "response": {
        "received": False,
        "content": None
    },
    "status": "UNKNOWN"
}


targets = [
    "http://localhost:8000/chat",
    "http://localhost:8000/api/chat"
]


payload = json.dumps({
    "message": "Explain artificial intelligence research"
}).encode("utf-8")


for target in targets:

    try:
        req = urllib.request.Request(
            target,
            data=payload,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=5) as response:

            body = response.read().decode("utf-8")

            result["endpoint"]["tested"] = True
            result["endpoint"]["reachable"] = True

            result["request"]["sent"] = True

            result["response"]["received"] = True
            result["response"]["content"] = body[:500]

            result["status"] = "CHAT_ENDPOINT_READY"

            break

    except Exception as exc:

        result["last_error"] = str(exc)


if result["status"] == "UNKNOWN":

    result["status"] = "WAITING_API_RUNTIME"


with open(
    "/workspace/delbot/repository_data/mapping/chat_endpoint_test_validation.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )


print(json.dumps(result, indent=2))


PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
    "$ROOT/delbot_platform/api" \
    "$ROOT/delbot_platform/gateway" \
    -q


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo
echo "======================================================================"
echo "PR-5.1BH COMPLETE"
echo "======================================================================"


echo
echo "NEXT"
echo "CHAT_ENDPOINT_READY -> lanjut PR-5.1BI RAG Context Injection"
echo "WAITING_API_RUNTIME -> start backend API"
echo
