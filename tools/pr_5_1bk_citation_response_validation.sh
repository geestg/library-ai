#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BK
#
# Citation Response Validation
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
# LLM Answer
#       |
#       v
# Citation Builder
#       |
#       v
# Final Response
#
# Rules:
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak exit
# - Tidak return
# - Terminal tetap terbuka
#

set -u

PROJECT="/workspace/delbot"
OUTPUT="$PROJECT/repository_data/mapping/citation_response_validation.json"

mkdir -p "$(dirname "$OUTPUT")"


python3 <<'PY'

import json
import os
from datetime import datetime


project = "/workspace/delbot"

checks = {
    "citation_builder": False,
    "citation_models": False,
    "context_reference": False,
    "response_mapper": False
}


search_paths = [
    "delbot_platform/knowledge/citation",
    "delbot_platform/knowledge/context",
    "delbot_platform/gateway/mapper",
    "delbot_platform/research"
]


for path in search_paths:
    full = os.path.join(project, path)

    if os.path.exists(full):
        files = []

        for root, dirs, filenames in os.walk(full):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(filename.lower())

        for file in files:

            if "citation" in file:
                checks["citation_builder"] = True

            if "model" in file:
                checks["citation_models"] = True

            if "context" in file:
                checks["context_reference"] = True

            if "mapper" in file or "response" in file:
                checks["response_mapper"] = True


flow = {
    "answer_to_citation": checks["citation_builder"],
    "citation_to_response": checks["response_mapper"],
    "context_reference_available": checks["context_reference"]
}


ready = all(flow.values())


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BK",
    "checks": checks,
    "flow": flow,
    "status": (
        "READY_CITATION_RESPONSE"
        if ready
        else "INCOMPLETE_CITATION_RESPONSE"
    )
}


with open(
    "/workspace/delbot/repository_data/mapping/citation_response_validation.json",
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


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"


python3 -m compileall \
    "$PROJECT/delbot_platform/knowledge" \
    "$PROJECT/delbot_platform/gateway" \
    "$PROJECT/delbot_platform/research"


echo ""
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo ""
echo "======================================================================"
echo "PR-5.1BK COMPLETE"
echo "======================================================================"


echo ""
echo "NEXT"
echo "READY_CITATION_RESPONSE -> lanjut PR-5.1BL Full MVP Answer Pipeline"
echo "INCOMPLETE_CITATION_RESPONSE -> audit citation layer"


# terminal intentionally stays open
