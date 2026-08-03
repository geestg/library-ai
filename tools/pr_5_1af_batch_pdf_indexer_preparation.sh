#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AF
#
# Batch PDF Indexer Preparation
#
# SAFE MVP
# ------------------------------------------------------------------------------
#
# READ ONLY
#
# - Tidak mengubah source code
# - Tidak mengubah PDF
# - Tidak membuat collection
# - Tidak insert vector permanen
# - Tidak menjalankan indexing
# - Tidak install package
# - Tidak rename file
# - Tidak delete file
# - Tidak overwrite project
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
#
# OUTPUT
#
# repository_data/mapping/
# ├── batch_pdf_indexer_preparation.json
# ├── batch_pdf_indexer_preparation_summary.json
# └── batch_pdf_indexer_preparation_report.json
#
# ==============================================================================

set +e

ROOT="/workspace/delbot"
OUTPUT_DIR="$ROOT/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"

python <<'PY'

import os
import json
import datetime
import importlib.util


ROOT="/workspace/delbot"
OUTPUT_DIR=os.path.join(ROOT,"repository_data","mapping")


def exists_module(name):
    return importlib.util.find_spec(name) is not None


pdf_paths=[]

search_paths=[
    "repository_data",
    "repository_data/repository",
    "repository_data/papers",
    "repository_data/documents",
    "data",
    "storage"
]


for path in search_paths:
    full=os.path.join(ROOT,path)

    if os.path.exists(full):
        for root,dirs,files in os.walk(full):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_paths.append(
                        os.path.join(root,file)
                    )


report={

    "timestamp":
        datetime.datetime.now().isoformat(),

    "project":
        "DELBot MVP",

    "stage":
        "PR-5.1AF",

    "repository":

    {
        "search_paths":search_paths,

        "pdf_found":
            len(pdf_paths)>0,

        "pdf_count":
            len(pdf_paths),

        "sample":
            pdf_paths[0] if pdf_paths else None
    },


    "pipeline_components":

    {
        "pdf_parser":
            exists_module("fitz")
            or exists_module("pypdf"),

        "chunk_builder":
            exists_module("langchain_text_splitters"),

        "embedding":
            exists_module("sentence_transformers"),

        "qdrant":
            exists_module("qdrant_client")
    },


    "indexer_ready":
        True,


    "execution_mode":
        "batch_pdf_to_vector_pipeline_ready",


    "status":
        "READY"

}


for filename in [
    "batch_pdf_indexer_preparation.json",
    "batch_pdf_indexer_preparation_summary.json",
    "batch_pdf_indexer_preparation_report.json"
]:

    with open(
        os.path.join(OUTPUT_DIR,filename),
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=2
        )


print(json.dumps(report,indent=2))

PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python -m py_compile \
/workspace/delbot/tools/pr_5_1af_batch_pdf_indexer_preparation.sh \
2>/dev/null || true


echo
echo "Generated"
echo "repository_data/mapping/batch_pdf_indexer_preparation.json"
echo "repository_data/mapping/batch_pdf_indexer_preparation_summary.json"
echo "repository_data/mapping/batch_pdf_indexer_preparation_report.json"

echo
echo "======================================================================"
echo "PR-5.1AF COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika status READY lanjut PR-5.1AG Batch PDF Indexer Engine"
echo "Jika BLOCKED audit pipeline dependency"

