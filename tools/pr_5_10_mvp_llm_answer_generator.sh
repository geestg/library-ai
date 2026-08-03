#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.10
#
# LLM Answer Generator (MVP)
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

OUTPUT="$MAPDIR/llm_answer_generator.json"

mkdir -p "$MAPDIR"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.10 LLM Answer Generator"
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
    "status":"FAILED"
}

try:

    chat=json.loads(inp.read_text(encoding="utf-8"))

    ctx=chat.get("context",[])

    query=chat.get("query","")

    hits=len(ctx)

    snippets=[]

    sources=[]

    for item in ctx:

        text=(item.get("text") or "").replace("\n"," ").strip()

        if len(text)>240:
            text=text[:240]+"..."

        snippets.append(text)

        doc=item.get("document") or "unknown"

        cid=item.get("chunk_id")

        sources.append({
            "document":doc,
            "chunk_id":cid
        })

    answer=[]

    answer.append(f"Pertanyaan: {query}")
    answer.append("")
    answer.append("Jawaban disusun dari hasil semantic retrieval repository.")
    answer.append("")

    for i,s in enumerate(snippets,1):
        answer.append(f"{i}. {s}")

    result.update({
        "query":query,
        "hits":hits,
        "sources":sources,
        "answer":"\n".join(answer),
        "status":"SUCCESS"
    })

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

print(json.dumps({
    "backend":result.get("backend"),
    "hits":result.get("hits",0),
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
echo "SUCCESS -> PR-5.11 Citation Builder MVP"

