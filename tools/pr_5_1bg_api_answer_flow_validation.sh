#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BG
#
# API Answer Flow Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# Client
#   |
#   v
# Backend API
#   |
#   v
# Gateway
#   |
#   v
# LLM Provider Connector
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


ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/api_answer_flow_validation.json"


echo "======================================================================"
echo "PR-5.1BG"
echo "API Answer Flow Validation"
echo "======================================================================"


python3 <<'PY'
import json
import os
from datetime import datetime


root="/workspace/delbot"

result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BG",

    "gateway": {
        "exists": False,
        "providers": False,
        "openai_connector": False
    },

    "api": {
        "exists": False,
        "routers": False,
        "chat_endpoint": False
    },

    "flow": {
        "client_to_gateway": False,
        "gateway_to_llm": False,
        "answer_generation_ready": False
    },

    "status": "CHECKING"
}


checks = {
    "gateway": [
        "delbot_platform/gateway",
        "delbot_platform/gateway/providers",
        "delbot_platform/gateway/openai"
    ],

    "api": [
        "delbot_platform/api",
        "delbot_platform/api/routers"
    ]
}


gateway_ok = all(
    os.path.exists(os.path.join(root, x))
    for x in checks["gateway"]
)

api_ok = all(
    os.path.exists(os.path.join(root, x))
    for x in checks["api"]
)


result["gateway"]["exists"] = os.path.exists(
    os.path.join(root,"delbot_platform/gateway")
)

result["gateway"]["providers"] = os.path.exists(
    os.path.join(root,"delbot_platform/gateway/providers")
)

result["gateway"]["openai_connector"] = os.path.exists(
    os.path.join(root,"delbot_platform/gateway/openai")
)


result["api"]["exists"] = os.path.exists(
    os.path.join(root,"delbot_platform/api")
)

result["api"]["routers"] = os.path.exists(
    os.path.join(root,"delbot_platform/api/routers")
)


result["api"]["chat_endpoint"] = os.path.exists(
    os.path.join(root,"delbot_platform/api/routes")
)


result["flow"]["client_to_gateway"] = api_ok and gateway_ok
result["flow"]["gateway_to_llm"] = gateway_ok

result["flow"]["answer_generation_ready"] = (
    result["flow"]["client_to_gateway"]
    and result["flow"]["gateway_to_llm"]
)


if result["flow"]["answer_generation_ready"]:
    result["status"]="READY_API_ANSWER_FLOW"
else:
    result["status"]="INCOMPLETE_API_FLOW"


os.makedirs(
    os.path.dirname("/workspace/delbot/repository_data/mapping/api_answer_flow_validation.json"),
    exist_ok=True
)


with open(
    "/workspace/delbot/repository_data/mapping/api_answer_flow_validation.json",
    "w"
) as f:
    json.dump(result,f,indent=2)


print(json.dumps(result,indent=2))

PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"


python3 -m compileall \
/workspace/delbot/delbot_platform/api \
/workspace/delbot/delbot_platform/gateway


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo
echo "======================================================================"
echo "PR-5.1BG COMPLETE"
echo "======================================================================"


echo
echo "NEXT"
echo "READY_API_ANSWER_FLOW -> lanjut PR-5.1BH Chat Endpoint Test"
echo "INCOMPLETE_API_FLOW -> audit gateway/api"
echo

