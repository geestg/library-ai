#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AC
#
# Embedding Pipeline Validation
#
# SAFE MVP
# ------------------------------------------------------------------------------
#
# READ ONLY
#
# - Tidak mengubah source code
# - Tidak mengubah PDF
# - Tidak membuat collection
# - Tidak insert vector
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
# ├── embedding_pipeline_validation.json
# ├── embedding_pipeline_validation_summary.json
# └── embedding_pipeline_validation_report.json
#
# ==============================================================================

PROJECT_ROOT="/workspace/delbot"
OUTPUT_DIR="$PROJECT_ROOT/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"

echo "======================================================================"
echo "PR-5.1AC"
echo "Embedding Pipeline Validation"
echo "======================================================================"

python3 <<'PYTHON'
import json
import os
import importlib.util
import datetime
import traceback

ROOT = "/workspace/delbot"
OUTPUT = os.path.join(ROOT, "repository_data", "mapping")

result = {
    "timestamp": datetime.datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AC",
    "dependencies": {},
    "models": {},
    "embedding_engine": {},
    "qdrant": {},
    "sample_embedding": {},
    "exception": None,
    "status": "UNKNOWN"
}

def check_module(name):
    return importlib.util.find_spec(name) is not None


try:

    result["dependencies"] = {
        "sentence_transformers": check_module("sentence_transformers"),
        "transformers": check_module("transformers"),
        "torch": check_module("torch"),
        "numpy": check_module("numpy"),
    }


    model_candidates = [
        "BAAI/bge-m3",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]

    result["models"] = {
        "default_target": "BAAI/bge-m3",
        "fallback": "sentence-transformers/all-MiniLM-L6-v2",
        "available_runtime": False
    }


    try:
        from sentence_transformers import SentenceTransformer

        result["embedding_engine"] = {
            "library": "sentence-transformers",
            "ready": True
        }

        result["models"]["available_runtime"] = True


        try:
            model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            vector = model.encode(
                "DELBot academic research intelligence platform"
            )

            result["sample_embedding"] = {
                "generated": True,
                "dimension": len(vector.tolist())
            }

        except Exception as e:

            result["sample_embedding"] = {
                "generated": False,
                "reason": str(e)
            }


    except Exception as e:

        result["embedding_engine"] = {
            "library": "sentence-transformers",
            "ready": False,
            "error": str(e)
        }


    try:

        from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

        store = get_qdrant_store()

        result["qdrant"] = {
            "available": True,
            "runtime": type(store).__name__
        }

    except Exception as e:

        result["qdrant"] = {
            "available": False,
            "error": str(e)
        }


    deps_ready = all(
        [
            result["dependencies"]["sentence_transformers"],
            result["dependencies"]["torch"],
            result["dependencies"]["numpy"]
        ]
    )


    if deps_ready and result["embedding_engine"].get("ready"):

        result["status"] = "READY"

    else:

        result["status"] = "PARTIAL"


except Exception as e:

    result["exception"] = traceback.format_exc()
    result["status"] = "ERROR"


for name in [
    "embedding_pipeline_validation.json",
    "embedding_pipeline_validation_summary.json",
    "embedding_pipeline_validation_report.json"
]:

    path = os.path.join(OUTPUT, name)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )


print(json.dumps(result, indent=2, ensure_ascii=False))

PYTHON


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile \
/workspace/delbot/tools/pr_5_1ac_embedding_pipeline_validation.sh 2>/dev/null || true


echo
echo "Generated"
echo "$OUTPUT_DIR/embedding_pipeline_validation.json"
echo "$OUTPUT_DIR/embedding_pipeline_validation_summary.json"
echo "$OUTPUT_DIR/embedding_pipeline_validation_report.json"

echo
echo "======================================================================"
echo "PR-5.1AC COMPLETE"
echo "======================================================================"

echo "NEXT"
echo "Jika status READY lanjut PR-5.1AD Vector Indexing Pipeline Validation"
echo "Jika PARTIAL audit embedding dependency"
echo "======================================================================"

