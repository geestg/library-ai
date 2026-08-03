#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.19
#
# MVP Release Manifest
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
EXPORTDIR="$ROOT/repository_data/mvp_export"

OUTPUT="$REPORTDIR/mvp_release_manifest.json"

mkdir -p "$REPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.19 MVP Release Manifest"
echo "======================================================================"

python3 <<PY
import json
from pathlib import Path
from datetime import datetime

root=Path(r"$ROOT")
mapping=Path(r"$MAPDIR")
report=Path(r"$REPORTDIR")
export=Path(r"$EXPORTDIR")

checks=[
    mapping/"repository_qa_validation.json",
    mapping/"local_embedding_build.json",
    mapping/"local_qdrant_index.json",
    mapping/"local_retrieval_engine.json",
    mapping/"repository_chat.json",
    mapping/"llm_answer_generator.json",
    mapping/"citation_builder.json",
    mapping/"ask_repository.json",
    mapping/"end_to_end_validation.json",
    mapping/"demo_query_suite.json",
    mapping/"mvp_final_readiness.json",
    report/"mvp_system_report.json",
    report/"mvp_smoke_test.json"
]

existing=[]

for f in checks:
    if f.exists():
        existing.append(str(f.relative_to(root)))

package=export/"delbot_mvp_package.tar.gz"

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "version":"0.1.0-mvp",
    "backend":"QDRANT_LOCAL",
    "artifacts":len(existing),
    "package_exists":package.exists(),
    "package":str(package),
    "files":existing,
    "status":"SUCCESS"
}

out=Path(r"$OUTPUT")
out.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(json.dumps({
    "project":result["project"],
    "version":result["version"],
    "artifacts":result["artifacts"],
    "package_exists":result["package_exists"],
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
echo "SUCCESS -> PR-5.20 MVP Release Summary"

