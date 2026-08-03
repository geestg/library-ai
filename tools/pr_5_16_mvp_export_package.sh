#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.16
#
# Export MVP Package
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

EXPORTDIR="$ROOT/repository_data/mvp_export"

OUTPUT="$MAPDIR/mvp_export_package.json"

PACKAGE="$EXPORTDIR/delbot_mvp_package.tar.gz"

mkdir -p "$MAPDIR"
mkdir -p "$EXPORTDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.16 Export MVP Package"
echo "======================================================================"

python3 <<PY
import json
import pathlib
import tarfile
from datetime import datetime

root=pathlib.Path(r"$ROOT")
mapping=pathlib.Path(r"$MAPDIR")
export_dir=pathlib.Path(r"$EXPORTDIR")
package=pathlib.Path(r"$PACKAGE")
output=pathlib.Path(r"$OUTPUT")

include=[]

for name in [
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
    "mvp_final_readiness.json"
]:
    p=mapping/name
    if p.exists():
        include.append(p)

qdrant=root/"repository_data"/"qdrant_local"
manifest=mapping/"pdf_chunk_manifest.json"

with tarfile.open(package,"w:gz") as tar:

    for f in include:
        tar.add(f,arcname=f"mapping/{f.name}")

    if manifest.exists():
        tar.add(manifest,arcname="mapping/pdf_chunk_manifest.json")

    if qdrant.exists():
        tar.add(qdrant,arcname="qdrant_local")

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "package":str(package),
    "exported_files":len(include),
    "backend":"QDRANT_LOCAL",
    "status":"SUCCESS"
}

output.write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps(result,indent=2))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$PACKAGE"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.17 MVP System Report"

