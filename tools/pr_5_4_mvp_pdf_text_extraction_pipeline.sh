#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.4
#
# PDF Text Extraction Pipeline
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Extract PDF text for repository documents
#
# Input:
# - pdf_repository_manifest.json
#
# Output:
# - pdf_text_extraction_manifest.json
#
# Tidak melakukan:
# - delete
# - migration
# - rebuild index
# - restart service
# - exit
#

set -u

ROOT="/workspace/delbot"

INPUT="$ROOT/repository_data/mapping/pdf_repository_manifest.json"
OUTPUT="$ROOT/repository_data/mapping/pdf_text_extraction_manifest.json"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.4 PDF Text Extraction Pipeline"
echo "======================================================================"


python3 <<'PY'

import os
import json
from datetime import datetime


INPUT = "/workspace/delbot/repository_data/mapping/pdf_repository_manifest.json"
OUTPUT = "/workspace/delbot/repository_data/mapping/pdf_text_extraction_manifest.json"


try:
    import pypdf
except Exception as e:
    print("Missing dependency: pypdf")
    print(e)

    result = {
        "status": "DEPENDENCY_MISSING",
        "dependency": "pypdf",
        "timestamp": datetime.utcnow().isoformat()+"Z"
    }

    with open(OUTPUT,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))
else:

    with open(INPUT,"r") as f:
        manifest=json.load(f)


    pdf_list = manifest.get("files", [])

    documents=[]

    success=0
    failed=0


    for item in pdf_list:

        path=item.get("path")

        record={
            "path":path,
            "status":"",
            "pages":0,
            "text_length":0,
            "preview":"",
        }


        try:

            reader=pypdf.PdfReader(path)

            text=""

            for page in reader.pages:
                try:
                    page_text=page.extract_text() or ""
                    text += page_text + "\n"

                except Exception:
                    pass


            record["pages"]=len(reader.pages)
            record["text_length"]=len(text)
            record["preview"]=text[:500]

            record["status"]="TEXT_EXTRACTION_SUCCESS"

            success += 1


        except Exception as e:

            record["status"]="TEXT_EXTRACTION_FAILED"
            record["error"]=str(e)

            failed += 1


        documents.append(record)



    result={

        "timestamp":
            datetime.utcnow().isoformat()+"Z",

        "project":
            "DELBot MVP",

        "stage":
            "PR-5.4",

        "status":
            "PDF_TEXT_EXTRACTION_COMPLETE",

        "statistics":{

            "total_pdf":
                len(pdf_list),

            "success":
                success,

            "failed":
                failed
        },

        "documents":
            documents

    }


    with open(OUTPUT,"w") as f:
        json.dump(
            result,
            f,
            indent=2
        )


    print(json.dumps({

        "status":
            result["status"],

        "total_pdf":
            len(pdf_list),

        "success":
            success,

        "failed":
            failed,

        "output":
            OUTPUT

    },indent=2))


PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.4 COMPLETE"

echo

echo "NEXT"
echo "PR-5.5 -> PDF Chunk Builder MVP"

echo

echo "Terminal remains open"

