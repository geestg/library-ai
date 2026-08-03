#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.14
#
# MVP Demo Query Suite
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
ASK="$MAPDIR/ask_repository.json"

OUTPUT="$MAPDIR/demo_query_suite.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.14 MVP Demo Query Suite"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

chat_file=pathlib.Path(r"$CHAT")
ask_file=pathlib.Path(r"$ASK")
output_file=pathlib.Path(r"$OUTPUT")

queries=[
    "Apa itu Computer Vision?",
    "Jelaskan Deep Learning.",
    "Apa tujuan penelitian?",
    "Apa metode penelitian?",
    "Apa kesimpulan penelitian?"
]

chat_ok=False
ask_ok=False
hits=0
citations=0

if chat_file.exists():
    try:
        d=json.loads(chat_file.read_text(encoding="utf-8"))
        chat_ok=d.get("status")=="SUCCESS"
        hits=d.get("hits",0)
    except Exception:
        pass

if ask_file.exists():
    try:
        d=json.loads(ask_file.read_text(encoding="utf-8"))
        ask_ok=d.get("status")=="SUCCESS"
        citations=d.get("citations",0)
    except Exception:
        pass

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "stage":"PR-5.14",
    "backend":"QDRANT_LOCAL",
    "demo_queries":queries,
    "query_count":len(queries),
    "retrieval_ready":chat_ok,
    "qa_ready":ask_ok,
    "retrieval_hits":hits,
    "citations":citations,
    "status":"SUCCESS" if chat_ok and ask_ok else "FAILED"
}

output_file.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(json.dumps({
    "backend":result["backend"],
    "queries":result["query_count"],
    "retrieval_ready":result["retrieval_ready"],
    "qa_ready":result["qa_ready"],
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
echo "SUCCESS -> PR-5.15 MVP Final Readiness"

