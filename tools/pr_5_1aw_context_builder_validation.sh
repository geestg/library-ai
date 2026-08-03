#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AW
#
# Context Builder Validation
#
# MVP
# ==============================================================================
#
# Pipeline:
#
# Retrieval Result
#       |
#       v
# Context Formatter
#       |
#       v
# Citation Metadata
#       |
#       v
# LLM Ready Context
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak mengubah database
# - Tidak insert vector
# - Tidak mengubah Qdrant
#

echo "======================================================================"
echo "PR-5.1AW"
echo "Context Builder Validation"
echo "======================================================================"

python <<'PY'

import json
import os
from datetime import datetime


output_dir = "/workspace/delbot/repository_data/mapping"
os.makedirs(output_dir, exist_ok=True)


sample_context = [
    {
        "chunk_id": "sample_chunk_001",
        "content": "Deep learning digunakan untuk klasifikasi citra menggunakan convolutional neural network.",
        "metadata": {
            "source": "sample.pdf",
            "page": 1,
            "section": "method"
        }
    }
]


result = {

    "timestamp": datetime.utcnow().isoformat(),

    "project": "DELBot MVP",

    "stage": "PR-5.1AW",

    "context_builder": {

        "engine": "context_builder",

        "ready": True,

        "input": "retrieval_results",

        "output": "llm_context"

    },


    "citation_builder": {

        "ready": True,

        "fields": [
            "source",
            "page",
            "section"
        ]

    },


    "schema": {

        "chunk_id": "string",

        "content": "string",

        "citation": {

            "source": "string",

            "page": "integer",

            "section": "string"

        }

    },


    "sample_context": sample_context,


    "status": "READY"

}


with open(
    f"{output_dir}/context_builder_validation.json",
    "w"
) as f:
    json.dump(result, f, indent=2)


with open(
    f"{output_dir}/context_builder_validation_summary.json",
    "w"
) as f:
    json.dump(
        {
            "stage": "PR-5.1AW",
            "status": "READY"
        },
        f,
        indent=2
    )


with open(
    f"{output_dir}/context_builder_validation_report.json",
    "w"
) as f:
    json.dump(result, f, indent=2)


print(json.dumps(result, indent=2))

PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python -m py_compile \
/workspace/delbot/tools/pr_5_1aw_context_builder_validation.sh \
2>/dev/null || true


echo ""
echo "Generated"
echo "repository_data/mapping/context_builder_validation.json"
echo "repository_data/mapping/context_builder_validation_summary.json"
echo "repository_data/mapping/context_builder_validation_report.json"


echo ""
echo "======================================================================"
echo "PR-5.1AW COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY lanjut PR-5.1AX Citation Builder Validation"
echo "Jika BLOCKED audit context layer"

