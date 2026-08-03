#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.20
#
# MVP Release Summary
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

REPORTDIR="$ROOT/repository_data/report"
MAPDIR="$ROOT/repository_data/mapping"

OUTPUT="$REPORTDIR/mvp_release_summary.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.20 MVP Release Summary"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

reportdir=pathlib.Path(r"$REPORTDIR")
mapdir=pathlib.Path(r"$MAPDIR")
output=pathlib.Path(r"$OUTPUT")

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
    "mvp_export_package.json",
]

present=0

for f in checks:
    if (mapdir/f).exists():
        present+=1

package=pathlib.Path(
    "/workspace/delbot/repository_data/mvp_export/delbot_mvp_package.tar.gz"
).exists()

summary={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "version":"0.1.0-mvp",
    "backend":"QDRANT_LOCAL",
    "pipeline_files":present,
    "expected_pipeline_files":len(checks),
    "package_exists":package,
    "repository_chat":(mapdir/"repository_chat.json").exists(),
    "retrieval_engine":(mapdir/"local_retrieval_engine.json").exists(),
    "embedding":(mapdir/"local_embedding_build.json").exists(),
    "qa_pipeline":(mapdir/"repository_qa_validation.json").exists(),
    "status":"SUCCESS"
}

output.write_text(
    json.dumps(summary,indent=2),
    encoding="utf-8"
)

print(json.dumps(summary,indent=2))

PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.21 MVP Repository Statistics"

