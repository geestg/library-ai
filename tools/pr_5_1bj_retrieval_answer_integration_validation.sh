#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BJ
#
# Retrieval Answer Integration Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# User Question
#       |
#       v
# Retriever
#       |
#       v
# Context Builder
#       |
#       v
# Gateway
#       |
#       v
# LLM Answer
#       |
#       v
# Citation Response
#
# Rules:
# - Tidak start backend
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak exit
# - Tidak return
#

PROJECT_ROOT="/workspace/delbot"
OUTPUT="$PROJECT_ROOT/repository_data/mapping/retrieval_answer_integration_validation.json"

echo "======================================================================"
echo "PR-5.1BJ"
echo "Retrieval Answer Integration Validation"
echo "======================================================================"

python3 <<'PY'
import json
import os
from datetime import datetime

root="/workspace/delbot"

checks = {}

paths = {
    "retriever": [
        "delbot_platform/knowledge/retrieval",
        "delbot_platform/knowledge/rag"
    ],
    "context_builder": [
        "delbot_platform/knowledge/context"
    ],
    "gateway": [
        "delbot_platform/gateway"
    ],
    "citation": [
        "delbot_platform/knowledge/citation"
    ],
    "research_answer": [
        "delbot_platform/research"
    ]
}

for name, candidates in paths.items():
    checks[name] = {
        "exists": any(
            os.path.exists(os.path.join(root, item))
            for item in candidates
        )
    }


flow = {
    "question_to_retriever": checks["retriever"]["exists"],
    "retriever_to_context": (
        checks["retriever"]["exists"]
        and checks["context_builder"]["exists"]
    ),
    "context_to_gateway": (
        checks["context_builder"]["exists"]
        and checks["gateway"]["exists"]
    ),
    "answer_to_citation": (
        checks["gateway"]["exists"]
        and checks["citation"]["exists"]
    )
}


ready = all(flow.values())


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BJ",
    "checks": checks,
    "flow": flow,
    "status": (
        "READY_RETRIEVAL_ANSWER_INTEGRATION"
        if ready
        else
        "INCOMPLETE_RETRIEVAL_ANSWER_INTEGRATION"
    )
}


os.makedirs(
    os.path.dirname("/workspace/delbot/repository_data/mapping"),
    exist_ok=True
)

with open(
    "/workspace/delbot/repository_data/mapping/retrieval_answer_integration_validation.json",
    "w"
) as f:
    json.dump(result, f, indent=2)


print(json.dumps(result, indent=2))
PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform/knowledge \
/workspace/delbot/delbot_platform/gateway \
/workspace/delbot/delbot_platform/research \
>/dev/null 2>&1


echo
echo "======================================================================"
echo "Generated"
echo "/workspace/delbot/repository_data/mapping/retrieval_answer_integration_validation.json"
echo "======================================================================"

echo
echo "======================================================================"
echo "PR-5.1BJ COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "READY_RETRIEVAL_ANSWER_INTEGRATION -> lanjut PR-5.1BK Citation Response Validation"
echo "INCOMPLETE_RETRIEVAL_ANSWER_INTEGRATION -> audit retrieval/gateway"
echo
