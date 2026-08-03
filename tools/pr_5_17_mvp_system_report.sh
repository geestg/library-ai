#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.17
#
# MVP System Report
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

OUTDIR="$ROOT/repository_data/report"

OUTPUT="$OUTDIR/mvp_system_report.json"

mkdir -p "$OUTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.17 MVP System Report"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

mapdir=pathlib.Path(r"$MAPDIR")
outfile=pathlib.Path(r"$OUTPUT")

checks=[
("repository_qa_validation.json","Repository QA"),
("local_embedding_build.json","Embedding"),
("local_qdrant_index.json","Qdrant Local"),
("local_retrieval_engine.json","Retriever"),
("repository_chat.json","Repository Chat"),
("llm_answer_generator.json","LLM"),
("citation_builder.json","Citation"),
("ask_repository.json","Ask Repository"),
("end_to_end_validation.json","End To End"),
("demo_query_suite.json","Demo Query"),
("mvp_final_readiness.json","Final Readiness"),
("mvp_export_package.json","Export")
]

items=[]
passed=0

for filename,name in checks:

    fp=mapdir/filename

    ok=False

    if fp.exists():
        try:
            data=json.loads(fp.read_text())
            ok=data.get("status")=="SUCCESS"
        except Exception:
            ok=False

    if ok:
        passed+=1

    items.append({
        "component":name,
        "status":"SUCCESS" if ok else "FAILED"
    })

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "backend":"QDRANT_LOCAL",
    "total_components":len(items),
    "passed":passed,
    "failed":len(items)-passed,
    "completion_percent":round((passed/len(items))*100,2),
    "ready":passed==len(items),
    "components":items,
    "status":"SUCCESS"
}

outfile.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(json.dumps({
    "project":result["project"],
    "backend":result["backend"],
    "passed":result["passed"],
    "failed":result["failed"],
    "completion_percent":result["completion_percent"],
    "ready":result["ready"],
    "status":"SUCCESS"
},indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.18 MVP Smoke Test"

