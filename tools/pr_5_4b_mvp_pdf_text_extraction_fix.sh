#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.4B
#
# PDF Text Extraction Pipeline FIX
#
# MVP SAFE
# ==============================================================================
#
# Input:
# - repository_data/mapping/pdf_repository_manifest.json
#
# Output:
# - repository_data/mapping/pdf_text_extraction_manifest.json
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

OUTPUT="$ROOT/repository_data/mapping/pdf_text_extraction_manifest.json"

mkdir -p "$(dirname "$OUTPUT")"

echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.4B PDF Text Extraction Pipeline FIX"
echo "======================================================================"

python3 <<'PY'

import os
import json
from datetime import datetime


ROOT="/workspace/delbot"

manifest_path = (
    ROOT +
    "/repository_data/mapping/pdf_repository_manifest.json"
)

output_path = (
    ROOT +
    "/repository_data/mapping/pdf_text_extraction_manifest.json"
)


try:
    import pypdf
except Exception:

    print(
        "pypdf belum tersedia. install dependency:"
    )

    print(
        "pip install pypdf"
    )

    raise


if not os.path.exists(manifest_path):

    raise FileNotFoundError(
        manifest_path
    )


with open(manifest_path,"r") as f:
    manifest=json.load(f)


pdf_list=[]


if isinstance(manifest,dict):

    possible_keys=[
        "files",
        "pdf_files",
        "documents",
        "items",
        "locations"
    ]

    for key in possible_keys:

        if key in manifest:

            pdf_list=manifest[key]
            break


elif isinstance(manifest,list):

    pdf_list=manifest



results=[]

success=0
failed=0


for item in pdf_list:

    if isinstance(item,str):

        pdf_path=item

    elif isinstance(item,dict):

        pdf_path=(
            item.get("path")
            or
            item.get("file")
            or
            item.get("pdf_path")
        )

    else:
        continue


    if not pdf_path:
        continue


    record={
        "pdf_path":pdf_path,
        "status":"",
        "pages":0,
        "characters":0,
        "text_path":""
    }


    try:

        reader=pypdf.PdfReader(pdf_path)

        texts=[]

        for page in reader.pages:

            text=page.extract_text() or ""

            texts.append(text)


        full_text="\n".join(texts)


        relative=os.path.basename(pdf_path)

        text_file=(
            ROOT+
            "/repository_data/text/"
            +
            relative
            +
            ".txt"
        )


        os.makedirs(
            os.path.dirname(text_file),
            exist_ok=True
        )


        with open(
            text_file,
            "w",
            encoding="utf-8"
        ) as tf:

            tf.write(full_text)



        record["status"]="SUCCESS"
        record["pages"]=len(reader.pages)
        record["characters"]=len(full_text)
        record["text_path"]=text_file


        success+=1


    except Exception as e:

        record["status"]="FAILED"
        record["error"]=str(e)

        failed+=1


    results.append(record)



output={

    "timestamp":
        datetime.utcnow().isoformat()+"Z",

    "project":
        "DELBot MVP",

    "stage":
        "PR-5.4B",

    "status":
        "PDF_TEXT_EXTRACTION_COMPLETE",

    "statistics":
    {
        "total_pdf":
            len(results),

        "success":
            success,

        "failed":
            failed
    },

    "documents":
        results

}



with open(
    output_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2
    )


print(
    json.dumps(
        {
            "status":
                output["status"],

            "total_pdf":
                len(results),

            "success":
                success,

            "failed":
                failed,

            "output":
                output_path
        },
        indent=2
    )
)

PY


echo
echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.4B COMPLETE"

echo

echo "NEXT"
echo "PR-5.5 -> PDF Chunk Builder MVP"

echo

echo "Terminal tetap terbuka"
