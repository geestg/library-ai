#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1BX
#
# MVP PDF Repository Locator
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Locate real PDF repository source.
#
# Scope:
# - Scan repository_data
# - Scan workspace dataset
# - Detect pdf files
# - Build source mapping
#
# Tidak melakukan:
# - migration
# - cleanup
# - delete data
# - rebuild index
# - restart service
# - exit
#

set -u

ROOT="/workspace/delbot"
OUTPUT="$ROOT/repository_data/mapping/mvp_pdf_repository_locator.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.1BX PDF Repository Locator"
echo "======================================================================"

python3 <<'PY'
import os
import json
from datetime import datetime

root="/workspace/delbot"

search_paths=[
    os.path.join(root,"repository_data"),
    os.path.join(root,"datasets"),
    os.path.join(root,"data"),
    os.path.join(root,"storage"),
    os.path.join(root,"repository"),
    os.path.join(root,"documents"),
]

pdf_files=[]

for base in search_paths:
    if not os.path.exists(base):
        continue

    for current, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdf_files.append(
                    os.path.join(current,f)
                )


result={
    "timestamp":datetime.utcnow().isoformat()+"Z",
    "project":"DELBot MVP",
    "stage":"PR-5.1BX",
    "checks":{
        "repository_root_available":os.path.exists(root),
        "pdf_found":len(pdf_files)>0
    },
    "statistics":{
        "pdf_count":len(pdf_files)
    },
    "locations":pdf_files[:200],
    "status":
        "PDF_SOURCE_FOUND"
        if len(pdf_files)>0
        else "PDF_SOURCE_NOT_FOUND"
}


output="/workspace/delbot/repository_data/mapping/mvp_pdf_repository_locator.json"

with open(output,"w") as f:
    json.dump(result,f,indent=2)


print(json.dumps(result,indent=2))
PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.1BX COMPLETE"

echo

echo "NEXT"

python3 <<'PY'
import json

path="/workspace/delbot/repository_data/mapping/mvp_pdf_repository_locator.json"

with open(path) as f:
    data=json.load(f)

if data["status"]=="PDF_SOURCE_FOUND":
    print("READY_PDF_SOURCE -> lanjut PR-5.1BY Dataset Link Validation")
else:
    print("BLOCKED_PDF_SOURCE -> perlu lokasi dataset PDF asli")
PY


echo
echo "Terminal remains open"
