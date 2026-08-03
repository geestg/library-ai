#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.11
#
# Citation Builder MVP
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

INPUT="$MAPDIR/repository_chat.json"

OUTPUT="$MAPDIR/citation_builder.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.11 Citation Builder MVP"
echo "======================================================================"

python3 <<PY
import json
import pathlib
from datetime import datetime

inp=pathlib.Path(r"$INPUT")
out=pathlib.Path(r"$OUTPUT")

result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "backend":"QDRANT_LOCAL",
    "citations":[],
    "citation_count":0,
    "status":"FAILED"
}

if inp.exists():

    try:

        data=json.loads(inp.read_text(encoding="utf-8"))

        citations=[]

        for i,item in enumerate(data.get("context",[]),1):

            citations.append({
                "id":i,
                "document":item.get("document") or "UNKNOWN_DOCUMENT",
                "chunk_id":item.get("chunk_id"),
                "score":round(float(item.get("score",0)),4),
                "preview":item.get("text","").replace("\n"," ")[:180]
            })

        result["citations"]=citations
        result["citation_count"]=len(citations)
        result["status"]="SUCCESS"

    except Exception as e:

        result["error"]=str(e)

out.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(
    json.dumps(
        {
            "backend":result["backend"],
            "citation_count":result["citation_count"],
            "status":result["status"]
        },
        indent=2,
        ensure_ascii=False
    )
)

PY

echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo
echo "NEXT"
echo "SUCCESS -> PR-5.12 Ask Repository MVP"

