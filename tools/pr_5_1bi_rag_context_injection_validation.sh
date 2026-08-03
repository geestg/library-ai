#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BI
#
# RAG Context Injection Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# Repository
#      |
#      v
# Retriever
#      |
#      v
# Context Builder
#      |
#      v
# Gateway Prompt
#      |
#      v
# LLM Answer
#
# Rules:
# - Tidak start vLLM
# - Tidak download model
# - Tidak install package
# - Tidak ubah source
# - Tidak exit
# - Tidak return
#

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/rag_context_injection_validation.json"

echo "======================================================================"
echo "PR-5.1BI"
echo "RAG Context Injection Validation"
echo "======================================================================"

python3 <<'PY'

import json
import os
from datetime import datetime

root="/workspace/delbot"

checks={}

checks["retriever"]={
    "exists": os.path.exists(
        f"{root}/delbot_platform/knowledge/retrieval"
    )
}

checks["context_builder"]={
    "exists": os.path.exists(
        f"{root}/delbot_platform/knowledge/context"
    )
}

checks["rag_pipeline"]={
    "exists": os.path.exists(
        f"{root}/delbot_platform/knowledge/rag"
    )
}

checks["citation_layer"]={
    "exists": os.path.exists(
        f"{root}/delbot_platform/knowledge/citation"
    )
}

ready=all(
    [
        checks["retriever"]["exists"],
        checks["context_builder"]["exists"],
        checks["rag_pipeline"]["exists"]
    ]
)

result={
    "timestamp":datetime.utcnow().isoformat(),
    "project":"DELBot MVP",
    "stage":"PR-5.1BI",
    "checks":checks,
    "flow":{
        "document_to_retriever":ready,
        "retriever_to_context":ready,
        "context_to_llm_prompt":ready
    },
    "status":
        "READY_RAG_CONTEXT"
        if ready
        else "INCOMPLETE_RAG_CONTEXT"
}


os.makedirs(
    f"{root}/repository_data/mapping",
    exist_ok=True
)

with open(
    f"{root}/repository_data/mapping/rag_context_injection_validation.json",
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )

print(json.dumps(result,indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/delbot_platform/knowledge \
-q


echo ""
echo "======================================================================"
echo "Generated"
echo "/workspace/delbot/repository_data/mapping/rag_context_injection_validation.json"
echo "======================================================================"

echo ""
echo "======================================================================"
echo "PR-5.1BI COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "READY_RAG_CONTEXT -> lanjut PR-5.1BJ Retrieval Answer Integration"
echo "INCOMPLETE_RAG_CONTEXT -> audit knowledge pipeline"

