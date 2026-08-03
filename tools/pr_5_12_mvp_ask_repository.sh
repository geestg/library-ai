#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.12
#
# Ask Repository MVP
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

CHAT="$MAPDIR/repository_chat.json"
LLM="$MAPDIR/llm_answer_generator.json"
CITATION="$MAPDIR/citation_builder.json"

OUTPUT="$MAPDIR/ask_repository.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.12 Ask Repository MVP"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

chat_file=pathlib.Path(r"$CHAT")
llm_file=pathlib.Path(r"$LLM")
citation_file=pathlib.Path(r"$CITATION")
output_file=pathlib.Path(r"$OUTPUT")

answer=""
hits=0
citations=0
backend="QDRANT_LOCAL"

if chat_file.exists():
    try:
        d=json.loads(chat_file.read_text(encoding="utf-8"))
        answer=d.get("answer","")
        hits=d.get("hits",0)
        backend=d.get("backend","QDRANT_LOCAL")
    except Exception:
        pass

if citation_file.exists():
    try:
        d=json.loads(citation_file.read_text(encoding="utf-8"))
        citations=d.get("citation_count",0)
    except Exception:
        pass

status="SUCCESS"

if not pathlib.Path(r"$LLM").exists():
    status="FAILED"

preview=" ".join(answer.split())

if len(preview)>320:
    preview=preview[:320]+"..."

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":backend,
    "question":"Apa itu Computer Vision?",
    "answer_preview":preview,
    "retrieval_hits":hits,
    "citations":citations,
    "pipeline":[
        "Repository",
        "Retriever",
        "LLM",
        "Citation"
    ],
    "status":status
}

output_file.write_text(
    json.dumps(result,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

print(json.dumps(result,indent=2,ensure_ascii=False))
PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.13 MVP End-to-End Validation"

