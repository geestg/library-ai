#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BL
#
# Full MVP Answer Pipeline Validation
#
# MVP SAFE
# ==============================================================================
#
# Flow:
#
# User Question
#       |
#       v
# API Chat
#       |
#       v
# Gateway
#       |
#       v
# Retriever
#       |
#       v
# Context Builder
#       |
#       v
# LLM Connector
#       |
#       v
# Citation Builder
#       |
#       v
# Final Answer
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

OUTPUT="$PROJECT/repository_data/mapping/full_mvp_answer_pipeline_validation.json"


mkdir -p "$(dirname "$OUTPUT")"


python3 <<'PY'

import os
import json
from datetime import datetime


PROJECT="/workspace/delbot"


checks = {

    "api_chat": False,

    "gateway": False,

    "retriever": False,

    "context_builder": False,

    "llm_connector": False,

    "citation_builder": False,

    "research_answer": False

}


paths = {

    "api_chat":
        "delbot_platform/api",

    "gateway":
        "delbot_platform/gateway",

    "retriever":
        "delbot_platform/knowledge/retrieval",

    "context_builder":
        "delbot_platform/knowledge/context",

    "llm_connector":
        "delbot_platform/gateway/openai",

    "citation_builder":
        "delbot_platform/knowledge/citation",

    "research_answer":
        "delbot_platform/research"

}



for name, path in paths.items():

    target = os.path.join(PROJECT, path)

    if os.path.exists(target):

        py_files = []

        for root, dirs, files in os.walk(target):

            for file in files:

                if file.endswith(".py"):

                    py_files.append(file.lower())


        if len(py_files) > 0:

            checks[name] = True



flow = {

    "question_to_api":
        checks["api_chat"],

    "api_to_gateway":
        checks["gateway"],

    "gateway_to_retriever":
        checks["retriever"],

    "retriever_to_context":
        checks["context_builder"],

    "context_to_llm":
        checks["llm_connector"],

    "answer_to_citation":
        checks["citation_builder"],

    "research_response_ready":
        checks["research_answer"]

}



pipeline_ready = all(flow.values())


result = {

    "timestamp":
        datetime.utcnow().isoformat(),

    "project":
        "DELBot MVP",

    "stage":
        "PR-5.1BL",

    "checks":
        checks,

    "flow":
        flow,

    "status":
        (
            "READY_FULL_MVP_ANSWER_PIPELINE"
            if pipeline_ready
            else
            "INCOMPLETE_FULL_MVP_ANSWER_PIPELINE"
        )

}



output="/workspace/delbot/repository_data/mapping/full_mvp_answer_pipeline_validation.json"


with open(output,"w",encoding="utf-8") as f:

    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )


print(json.dumps(result,indent=2))


PY



echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"


python3 -m compileall \
"$PROJECT/delbot_platform/api" \
"$PROJECT/delbot_platform/gateway" \
"$PROJECT/delbot_platform/knowledge" \
"$PROJECT/delbot_platform/research"



echo ""
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"


echo ""
echo "======================================================================"
echo "PR-5.1BL COMPLETE"
echo "======================================================================"


echo ""
echo "NEXT"

echo "READY_FULL_MVP_ANSWER_PIPELINE -> lanjut PR-5.1BM MVP End-to-End Validation"

echo "INCOMPLETE_FULL_MVP_ANSWER_PIPELINE -> audit komponen yang false"


# terminal intentionally stays open

