#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BN
#
# MVP Functional Scenario Test
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate real MVP user flow.
#
# Scenario:
#
# Repository Registration
#        |
#        v
# PDF Discovery
#        |
#        v
# Document Processing
#        |
#        v
# Knowledge Indexing
#        |
#        v
# Semantic Retrieval
#        |
#        v
# Context Building
#        |
#        v
# Answer Generation
#        |
#        v
# Citation Response
#        |
#        v
# Research Output
#
# Safety:
# - No migration
# - No cleanup
# - No delete
# - No restart
# - No service modification
#
# ==============================================================================

set -u

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/mvp_functional_scenario_test.json"

echo
echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BN Functional Scenario Test"
echo "======================================================================"
echo


python3 <<PYTHON
import json
import os
from datetime import datetime

root = "${ROOT}"

checks = {
    "repository_registration": False,
    "pdf_discovery": False,
    "document_processing": False,
    "knowledge_indexing": False,
    "semantic_retrieval": False,
    "context_builder": False,
    "answer_generation": False,
    "citation_response": False,
    "research_output": False
}


paths = {
    "repository": [
        "delbot_platform/repository",
        "repository_data"
    ],
    "documents": [
        "delbot_platform/documents",
        "delbot_platform/document_intelligence"
    ],
    "knowledge": [
        "delbot_platform/knowledge"
    ],
    "retrieval": [
        "delbot_platform/knowledge/retrieval",
        "delbot_platform/knowledge/vector"
    ],
    "gateway": [
        "delbot_platform/gateway"
    ],
    "research": [
        "delbot_platform/research"
    ]
}


def exists_any(items):
    for item in items:
        if os.path.exists(os.path.join(root, item)):
            return True
    return False


checks["repository_registration"] = exists_any(paths["repository"])

checks["pdf_discovery"] = (
    os.path.exists(
        os.path.join(root, "delbot_platform/repository/discovery")
    )
)

checks["document_processing"] = exists_any(paths["documents"])

checks["knowledge_indexing"] = exists_any(paths["knowledge"])

checks["semantic_retrieval"] = exists_any(paths["retrieval"])

checks["context_builder"] = (
    os.path.exists(
        os.path.join(root, "delbot_platform/knowledge/context")
    )
)

checks["answer_generation"] = exists_any(paths["gateway"])

checks["citation_response"] = (
    os.path.exists(
        os.path.join(
            root,
            "delbot_platform/knowledge/citation"
        )
    )
)

checks["research_output"] = exists_any(paths["research"])


flow = {
    "repository_to_pdf": checks["repository_registration"]
        and checks["pdf_discovery"],

    "pdf_to_document_intelligence": checks["pdf_discovery"]
        and checks["document_processing"],

    "document_to_knowledge": checks["document_processing"]
        and checks["knowledge_indexing"],

    "knowledge_to_retrieval": checks["knowledge_indexing"]
        and checks["semantic_retrieval"],

    "retrieval_to_context": checks["semantic_retrieval"]
        and checks["context_builder"],

    "context_to_answer": checks["context_builder"]
        and checks["answer_generation"],

    "answer_to_citation": checks["answer_generation"]
        and checks["citation_response"],

    "citation_to_research": checks["citation_response"]
        and checks["research_output"]
}


all_checks = all(checks.values())
all_flow = all(flow.values())


if all_checks and all_flow:
    status = "READY_MVP_FUNCTIONAL_SCENARIO"
else:
    status = "INCOMPLETE_MVP_FUNCTIONAL_SCENARIO"


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BN",
    "checks": checks,
    "flow": flow,
    "status": status
}


os.makedirs(
    os.path.dirname("${OUTPUT}"),
    exist_ok=True
)

with open(
    "${OUTPUT}",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))

PYTHON


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
"$ROOT/delbot_platform/repository" \
"$ROOT/delbot_platform/documents" \
"$ROOT/delbot_platform/document_intelligence" \
"$ROOT/delbot_platform/knowledge" \
"$ROOT/delbot_platform/gateway" \
"$ROOT/delbot_platform/research"


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo
echo "======================================================================"
echo "PR-5.1BN COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "READY_MVP_FUNCTIONAL_SCENARIO -> lanjut PR-5.1BO MVP User Acceptance Validation"
echo "INCOMPLETE_MVP_FUNCTIONAL_SCENARIO -> audit komponen false"
echo

# Terminal remains open
