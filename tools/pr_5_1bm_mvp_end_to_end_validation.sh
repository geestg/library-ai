#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BM
#
# MVP End-to-End Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# Repository PDF
#       |
#       v
# Document Intelligence
#       |
#       v
# Knowledge Base
#       |
#       v
# Retriever
#       |
#       v
# RAG Context
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
OUTPUT="$PROJECT/repository_data/mapping/mvp_end_to_end_validation.json"


mkdir -p "$(dirname "$OUTPUT")"


python3 <<'PY'

import os
import json
from datetime import datetime


project = "/workspace/delbot"


checks = {
    "repository": False,
    "pdf_pipeline": False,
    "document_intelligence": False,
    "knowledge_base": False,
    "embedding": False,
    "vector_store": False,
    "retriever": False,
    "rag_context": False,
    "gateway": False,
    "llm_connector": False,
    "citation": False,
    "research_answer": False
}


targets = {
    "repository": [
        "delbot_platform/repository"
    ],

    "pdf_pipeline": [
        "delbot_platform/documents/parser",
        "delbot_platform/documents/pipeline"
    ],

    "document_intelligence": [
        "delbot_platform/document_intelligence"
    ],

    "knowledge_base": [
        "delbot_platform/knowledge"
    ],

    "embedding": [
        "delbot_platform/documents/embedding",
        "delbot_platform/ai/embedding"
    ],

    "vector_store": [
        "delbot_platform/vectorstore",
        "delbot_platform/knowledge/vector"
    ],

    "retriever": [
        "delbot_platform/knowledge/retrieval"
    ],

    "rag_context": [
        "delbot_platform/knowledge/context",
        "delbot_platform/knowledge/rag"
    ],

    "gateway": [
        "delbot_platform/gateway"
    ],

    "llm_connector": [
        "delbot_platform/gateway/openai",
        "delbot_platform/gateway/providers"
    ],

    "citation": [
        "delbot_platform/knowledge/citation"
    ],

    "research_answer": [
        "delbot_platform/research"
    ]
}


for key, paths in targets.items():

    for path in paths:

        full = os.path.join(project, path)

        if os.path.exists(full):

            py_found = False

            for root, dirs, files in os.walk(full):

                for file in files:
                    if file.endswith(".py"):
                        py_found = True
                        break

                if py_found:
                    break

            if py_found:
                checks[key] = True
                break



flow = {
    "repository_to_document": (
        checks["repository"]
        and checks["pdf_pipeline"]
    ),

    "document_to_knowledge": (
        checks["document_intelligence"]
        and checks["knowledge_base"]
    ),

    "knowledge_to_retrieval": (
        checks["embedding"]
        and checks["vector_store"]
        and checks["retriever"]
    ),

    "retrieval_to_rag": (
        checks["rag_context"]
    ),

    "rag_to_llm": (
        checks["gateway"]
        and checks["llm_connector"]
    ),

    "answer_to_citation": (
        checks["citation"]
    ),

    "research_ready": (
        checks["research_answer"]
    )
}


ready = all(flow.values())


result = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1BM",
    "checks": checks,
    "flow": flow,
    "status": (
        "READY_MVP_END_TO_END"
        if ready
        else "INCOMPLETE_MVP_END_TO_END"
    )
}


with open(
    "/workspace/delbot/repository_data/mapping/mvp_end_to_end_validation.json",
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
    "$PROJECT/delbot_platform/repository" \
    "$PROJECT/delbot_platform/documents" \
    "$PROJECT/delbot_platform/document_intelligence" \
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
echo "PR-5.1BM COMPLETE"
echo "======================================================================"


echo ""
echo "NEXT"
echo "READY_MVP_END_TO_END -> lanjut PR-5.1BN MVP Functional Scenario Test"
echo "INCOMPLETE_MVP_END_TO_END -> audit komponen false"


# terminal intentionally stays open
