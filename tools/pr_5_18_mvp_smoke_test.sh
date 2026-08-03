#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.18
#
# MVP Smoke Test
#
# SAFE
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Output ringkas
# ==============================================================================

set -u

ROOT="/workspace/delbot"

MAPDIR="$ROOT/repository_data/mapping"

REPORTDIR="$ROOT/repository_data/report"

OUTPUT="$REPORTDIR/mvp_smoke_test.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.18 MVP Smoke Test"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

root=pathlib.Path(r"$MAPDIR")

checks=[
    "repository_qa_validation.json",
    "local_embedding_build.json",
    "local_qdrant_index.json",
    "local_retrieval_engine.json",
    "repository_chat.json",
    "llm_answer_generator.json",
    "citation_builder.json",
    "ask_repository.json",
    "end_to_end_validation.json",
    "demo_query_suite.json",
    "mvp_final_readiness.json",
    "mvp_export_package.json"
]

passed=[]
failed=[]

for f in checks:

    p=root/f

    if not p.exists():
        failed.append({
            "file":f,
            "reason":"NOT_FOUND"
        })
        continue

    try:
        obj=json.loads(p.read_text())

        if obj.get("status")=="SUCCESS":
            passed.append(f)
        else:
            failed.append({
                "file":f,
                "reason":obj.get("status","UNKNOWN")
            })

    except Exception:
        failed.append({
            "file":f,
            "reason":"INVALID_JSON"
        })

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "stage":"PR-5.18",
    "total":len(checks),
    "passed":len(passed),
    "failed":len(failed),
    "ready":len(failed)==0,
    "status":"SUCCESS" if len(failed)==0 else "FAILED"
}

pathlib.Path(r"$OUTPUT").write_text(
    json.dumps(result,indent=2)
)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.19 MVP Release Manifest"
echo "FAILED  -> inspect $OUTPUT"

