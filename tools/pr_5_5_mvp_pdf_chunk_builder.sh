#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.5
#
# PDF Chunk Builder MVP
#
# MVP SAFE
# ==============================================================================
#
# Input:
# - pdf_repository_manifest.json
# - pdf_text_extraction_manifest.json (optional)
#
# Output:
# - pdf_chunk_manifest.json
#
# Tidak melakukan:
# - delete
# - migration
# - rebuild index
# - restart service
# - exit
#
# Terminal tetap terbuka
#

set -u

ROOT="/workspace/delbot"

OUTPUT="/workspace/delbot/repository_data/mapping/pdf_chunk_manifest.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.5 PDF Chunk Builder"
echo "======================================================================"

python3 <<'PY'

import os
import json
from datetime import datetime


MANIFEST = "/workspace/delbot/repository_data/mapping/pdf_repository_manifest.json"

OUTPUT = "/workspace/delbot/repository_data/mapping/pdf_chunk_manifest.json"


try:
    import fitz
except Exception:
    print("PyMuPDF belum tersedia")
    print("Install: pip install pymupdf")

    result = {
        "status": "FAILED",
        "reason": "PyMuPDF missing"
    }

    with open(OUTPUT,"w") as f:
        json.dump(result,f,indent=2)

    raise SystemExit


if not os.path.exists(MANIFEST):

    result = {
        "status":"FAILED",
        "reason":"pdf_repository_manifest.json missing"
    }

    with open(OUTPUT,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))

else:

    with open(MANIFEST) as f:
        data=json.load(f)


    pdf_list = data.get("documents",[])

    if not pdf_list:
        pdf_list = data.get("locations",[])


    chunks=[]

    success=0
    failed=0


    chunk_size=1200


    for index,item in enumerate(pdf_list):

        pdf_path = item.get("path")


        if not pdf_path:
            continue


        if not os.path.exists(pdf_path):
            failed += 1
            continue


        try:

            doc = fitz.open(pdf_path)

            full_text=""

            pages=[]


            for page_number,page in enumerate(doc):

                text = page.get_text()

                pages.append({
                    "page": page_number + 1,
                    "chars": len(text)
                })

                full_text += "\n" + text


            doc.close()


            if len(full_text.strip()) == 0:

                failed += 1
                continue


            success += 1


            text = full_text.strip()


            for start in range(0,len(text),chunk_size):

                chunk_text = text[start:start+chunk_size]


                chunks.append({

                    "document": os.path.basename(pdf_path),

                    "source_pdf": pdf_path,

                    "chunk_id": len(chunks),

                    "text": chunk_text,

                    "length": len(chunk_text),

                    "metadata":{

                        "page_count":len(pages),

                        "created_at":
                        datetime.utcnow().isoformat()+"Z"

                    }

                })


        except Exception as e:

            failed += 1



    result={

        "status":"PDF_CHUNK_BUILD_COMPLETE",

        "timestamp":
        datetime.utcnow().isoformat()+"Z",

        "statistics":{

            "pdf_total":len(pdf_list),

            "pdf_processed":success,

            "failed":failed,

            "chunk_total":len(chunks)

        },

        "chunks":chunks[:5000]

    }


    with open(OUTPUT,"w") as f:

        json.dump(
            result,
            f,
            indent=2
        )


    print(json.dumps({

        "status":result["status"],

        "pdf_total":
        result["statistics"]["pdf_total"],

        "processed":
        result["statistics"]["pdf_processed"],

        "failed":
        result["statistics"]["failed"],

        "chunks":
        result["statistics"]["chunk_total"],

        "output":OUTPUT

    },indent=2))


PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.5 COMPLETE"

echo

echo "NEXT"
echo "PR-5.6 -> Embedding Pipeline + Qdrant Index MVP"

echo

echo "Terminal remains open"
