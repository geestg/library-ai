#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.13
#
# End-to-End Validation
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

OUTPUT="$MAPDIR/end_to_end_validation.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.13 End-to-End Validation"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

root=pathlib.Path(r"$MAPDIR")

checks={
    "repository_qa_validation":"repository_qa_validation.json",
    "local_embedding_build":"local_embedding_build.json",
    "local_qdrant_index":"local_qdrant_index.json",
    "local_retrieval_engine":"local_retrieval_engine.json",
    "repository_chat":"repository_chat.json",
    "llm_answer_generator":"llm_answer_generator.json",
    "citation_builder":"citation_builder.json",
    "ask_repository":"ask_repository.json",
}

summary={}
passed=0

for name,file in checks.items():

    status=False

    p=root/file

    if p.exists():
        try:
            obj=json.loads(p.read_text())
            status=(obj.get("status")=="SUCCESS")
        except Exception:
            status=False

    summary[name]=status

    if status:
        passed+=1

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "stage":"PR-5.13",
    "total_checks":len(checks),
    "passed":passed,
    "failed":len(checks)-passed,
    "completion_percent":round((passed/len(checks))*100,2),
    "pipeline":summary,
    "mvp_ready":passed==len(checks),
    "status":"SUCCESS" if passed==len(checks) else "PARTIAL_SUCCESS"
}

pathlib.Path(r"$OUTPUT").write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
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
echo "SUCCESS -> PR-5.14 MVP Demo Query Suite"

