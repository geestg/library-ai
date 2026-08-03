#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BT
#
# MVP Smoke Test
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate minimum runtime readiness after MVP freeze.
#
# Scope:
# - Repository availability
# - Document pipeline availability
# - Knowledge layer availability
# - Retrieval availability
# - Gateway availability
# - Research response availability
#
# Tidak melakukan:
# - migration
# - cleanup
# - delete data
# - restart service
# - exit
# - return
#
# Terminal remains open
# ==============================================================================

set -u

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/mvp_smoke_test.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BT Smoke Test"
echo "======================================================================"

python3 <<'PY'
import json
import os
from datetime import datetime

root = "/workspace/delbot"

checks = {
    "repository_directory": os.path.exists(
        os.path.join(root, "repository_data")
    ),

    "repository_module": os.path.exists(
        os.path.join(root, "delbot_platform", "repository")
    ),

    "document_module": os.path.exists(
        os.path.join(root, "delbot_platform", "documents")
    ),

    "document_intelligence_module": os.path.exists(
        os.path.join(root, "delbot_platform", "document_intelligence")
    ),

    "knowledge_module": os.path.exists(
        os.path.join(root, "delbot_platform", "knowledge")
    ),

    "gateway_module": os.path.exists(
        os.path.join(root, "delbot_platform", "gateway")
    ),

    "research_module": os.path.exists(
        os.path.join(root, "delbot_platform", "research")
    ),

    "mapping_directory": os.path.exists(
        os.path.join(root, "repository_data", "mapping")
    )
}


flow = {
    "repository_available": checks["repository_directory"],
    "document_processing_available": (
        checks["document_module"]
        and checks["document_intelligence_module"]
    ),
    "knowledge_base_available": checks["knowledge_module"],
    "retrieval_pipeline_available": checks["knowledge_module"],
    "answer_pipeline_available": (
        checks["gateway_module"]
        and checks["research_module"]
    ),
    "mvp_runtime_ready": all(checks.values())
}


status = (
    "READY_MVP_SMOKE_TEST"
    if flow["mvp_runtime_ready"]
    else "INCOMPLETE_MVP_SMOKE_TEST"
)


result = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "project": "DELBot MVP",
    "stage": "PR-5.1BT",
    "checks": checks,
    "flow": flow,
    "status": status
}


output = "/workspace/delbot/repository_data/mapping/mvp_smoke_test.json"

with open(output, "w") as f:
    json.dump(result, f, indent=2)


print(json.dumps(result, indent=2))

PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform/repository \
/workspace/delbot/delbot_platform/documents \
/workspace/delbot/delbot_platform/document_intelligence \
/workspace/delbot/delbot_platform/knowledge \
/workspace/delbot/delbot_platform/gateway \
/workspace/delbot/delbot_platform/research


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "======================================================================"
echo "PR-5.1BT COMPLETE"
echo "======================================================================"

echo
echo "NEXT"

if [ -f "$OUTPUT" ]; then
    grep -q "READY_MVP_SMOKE_TEST" "$OUTPUT" \
    && echo "READY_MVP_SMOKE_TEST -> lanjut PR-5.1BU MVP Demo Dataset Validation" \
    || echo "INCOMPLETE_MVP_SMOKE_TEST -> audit komponen false"
fi

echo
echo "Terminal remains open"

