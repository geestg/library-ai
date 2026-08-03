#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.15
#
# MVP Final Readiness
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
OUTPUT="$MAPDIR/mvp_final_readiness.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.15 MVP Final Readiness"
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
    "demo_query_suite.json"
]

summary=[]
passed=0

for name in checks:

    p=root/name

    ok=False

    if p.exists():
        try:
            data=json.loads(p.read_text(encoding="utf-8"))
            ok=data.get("status")=="SUCCESS"
        except Exception:
            ok=False

    summary.append({
        "file":name,
        "ready":ok
    })

    if ok:
        passed+=1

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "stage":"PR-5.15",
    "total":len(checks),
    "passed":passed,
    "failed":len(checks)-passed,
    "ready":passed==len(checks),
    "completion_percent":round(passed/len(checks)*100,2),
    "status":"SUCCESS" if passed==len(checks) else "FAILED",
    "artifacts":summary
}

(pathlib.Path(r"$OUTPUT")).write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps({
    "ready":result["ready"],
    "passed":result["passed"],
    "failed":result["failed"],
    "completion_percent":result["completion_percent"],
    "status":result["status"]
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.16 Export MVP Package"
echo "FAILED  -> inspect mvp_final_readiness.json"

