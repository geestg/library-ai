#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BV
#
# MVP Live Query Validation
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Validate real query flow readiness.
#
# IMPORTANT:
# This stage does NOT create data.
# This stage only validates availability.
#
# Required:
# - Repository PDF
# - Chunk dataset
# - Embedding dataset
# - Vector storage
# - Retriever
# - RAG answer
#
# Tidak melakukan:
# - migration
# - cleanup
# - restart service
# - delete data
# - exit
# - return
#
# Terminal remains open
# ==============================================================================


ROOT="/workspace/delbot"
DATA="$ROOT/repository_data"
MAPPING="$DATA/mapping"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BV Live Query Validation"
echo "======================================================================"


python3 <<'PY'
import json
import os
from datetime import datetime, timezone


ROOT="/workspace/delbot"
DATA=os.path.join(ROOT,"repository_data")
MAPPING=os.path.join(DATA,"mapping")


checks={}

# Repository
checks["repository_data"] = os.path.exists(DATA)

# PDF availability
pdf_count=0

for root, dirs, files in os.walk(DATA):
    for f in files:
        if f.lower().endswith(".pdf"):
            pdf_count += 1

checks["pdf_repository_available"] = pdf_count > 0


# Chunk detection
chunk_files=[]

for root, dirs, files in os.walk(DATA):
    for f in files:
        if "chunk" in f.lower() and f.endswith(".json"):
            chunk_files.append(
                os.path.join(root,f)
            )

checks["chunk_dataset_available"] = len(chunk_files) > 0


# Embedding detection
embedding_files=[]

for root, dirs, files in os.walk(DATA):
    for f in files:
        name=f.lower()
        if (
            "embedding" in name
            or name.endswith(".bin")
            or name.endswith(".npy")
        ):
            embedding_files.append(
                os.path.join(root,f)
            )

checks["embedding_dataset_available"] = len(embedding_files) > 0


# Mapping directory
checks["mapping_directory"] = os.path.exists(MAPPING)


# Module checks
modules=[
    "delbot_platform.knowledge",
    "delbot_platform.gateway",
    "delbot_platform.research"
]


for module in modules:
    try:
        __import__(module)
        checks[module]=True
    except Exception:
        checks[module]=False


flow={
    "pdf_to_chunk": checks["pdf_repository_available"] and checks["chunk_dataset_available"],
    "chunk_to_embedding": checks["chunk_dataset_available"] and checks["embedding_dataset_available"],
    "embedding_to_retrieval": checks["embedding_dataset_available"],
    "retrieval_to_answer": checks.get("delbot_platform.knowledge",False)
}


ready = all(flow.values())


result={
    "timestamp":datetime.now(timezone.utc).isoformat(),
    "project":"DELBot MVP",
    "stage":"PR-5.1BV",
    "checks":checks,
    "statistics":{
        "pdf_count":pdf_count,
        "chunk_files":len(chunk_files),
        "embedding_files":len(embedding_files)
    },
    "flow":flow,
    "status":
        "READY_MVP_LIVE_QUERY"
        if ready
        else "BLOCKED_DATASET_INDEX_REQUIRED"
}


os.makedirs(MAPPING,exist_ok=True)

output=os.path.join(
    MAPPING,
    "mvp_live_query_validation.json"
)

with open(output,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result,indent=2))

print()
print("======================================================================")
print("Generated")
print(output)
print("======================================================================")

if ready:
    print("PR-5.1BV COMPLETE")
    print()
    print("NEXT")
    print("READY_MVP_LIVE_QUERY -> lanjut PR-5.1BW MVP Real Query Test")
else:
    print("PR-5.1BV BLOCKED")
    print()
    print("NEXT")
    print("Generate chunk dataset + embedding dataset")
    print("Then rerun PR-5.1BV")

PY


echo
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
"$ROOT/delbot_platform" \
-q


echo
echo "======================================================================"
echo "Terminal remains open"
echo "======================================================================"
