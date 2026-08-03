#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.3
#
# PDF Metadata Extraction + Parser Validation
#
# MVP SAFE
# ==============================================================================
#
# Input:
# - pdf_repository_manifest.json
# - skripsi_dataset.json
#
# Output:
# - pdf_metadata_validation.json
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

MANIFEST="$ROOT/repository_data/mapping/pdf_repository_manifest.json"

METADATA="$ROOT/delbot_platform/repository_data/metadata/skripsi_dataset.json"

OUTPUT="$ROOT/repository_data/mapping/pdf_metadata_validation.json"


mkdir -p "$(dirname "$OUTPUT")"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.3 PDF Metadata Extraction + Parser Validation"
echo "======================================================================"


python3 <<'PY'

import os
import json
from datetime import datetime


MANIFEST="/workspace/delbot/repository_data/mapping/pdf_repository_manifest.json"

METADATA="/workspace/delbot/delbot_platform/repository_data/metadata/skripsi_dataset.json"

OUTPUT="/workspace/delbot/repository_data/mapping/pdf_metadata_validation.json"


try:
    import fitz
    PDF_AVAILABLE=True
except Exception:
    PDF_AVAILABLE=False



def load_json(path):

    if not os.path.exists(path):
        return {}

    try:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}



manifest = load_json(MANIFEST)

metadata = load_json(METADATA)



pdf_items = []


if isinstance(manifest,dict):

    pdf_items = (
        manifest.get("pdf_files")
        or manifest.get("documents")
        or manifest.get("files")
        or []
    )


if not pdf_items and isinstance(manifest,list):
    pdf_items = manifest



metadata_items=[]


if isinstance(metadata,list):

    metadata_items=metadata


elif isinstance(metadata,dict):

    for key in [
        "data",
        "documents",
        "items",
        "skripsi"
    ]:

        if isinstance(metadata.get(key),list):
            metadata_items=metadata[key]
            break



metadata_index={}



for item in metadata_items:

    if not isinstance(item,dict):
        continue

    filename = (
        item.get("filename")
        or item.get("file")
        or item.get("pdf")
        or item.get("path")
    )


    if filename:

        metadata_index[
            os.path.basename(filename)
        ] = item



results=[]


valid_pdf=0
invalid_pdf=0
matched_metadata=0



for item in pdf_items:

    if isinstance(item,str):

        path=item

    elif isinstance(item,dict):

        path=(
            item.get("path")
            or item.get("file")
            or item.get("pdf")
        )

    else:

        continue



    if not path:
        continue



    record={

        "pdf_path": path,

        "exists": False,

        "size":0,

        "page_count":None,

        "text_available":False,

        "parser_status":"UNKNOWN",

        "metadata_found":False,

        "metadata":{}

    }



    if os.path.exists(path):

        record["exists"]=True

        record["size"]=os.path.getsize(path)


        if record["size"] > 0:

            valid_pdf += 1


        filename=os.path.basename(path)


        if filename in metadata_index:

            record["metadata_found"]=True

            record["metadata"]=metadata_index[filename]

            matched_metadata += 1



        if PDF_AVAILABLE:

            try:

                doc=fitz.open(path)

                record["page_count"]=doc.page_count


                text=""

                limit=min(doc.page_count,3)


                for i in range(limit):

                    text += doc[i].get_text()


                if text.strip():

                    record["text_available"]=True


                doc.close()


                record["parser_status"]="OK"


            except Exception as e:

                record["parser_status"]="FAILED"


        else:

            record["parser_status"]="PYMUPDF_NOT_INSTALLED"



    else:

        invalid_pdf += 1

        record["parser_status"]="FILE_NOT_FOUND"



    results.append(record)



output={

    "timestamp":
        datetime.utcnow().isoformat()+"Z",


    "project":
        "DELBot MVP",


    "stage":
        "PR-5.3",


    "statistics":{

        "pdf_total":
            len(results),

        "valid_pdf":
            valid_pdf,

        "invalid_pdf":
            invalid_pdf,

        "metadata_matched":
            matched_metadata

    },


    "dependency":{

        "pymupdf_available":
            PDF_AVAILABLE

    },


    "documents":
        results


}



with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )



print(json.dumps({

    "status":
        "PDF_METADATA_VALIDATION_COMPLETE",

    "pdf_total":
        len(results),

    "valid_pdf":
        valid_pdf,

    "metadata_matched":
        matched_metadata,

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

echo "PR-5.3 COMPLETE"

echo

echo "NEXT"
echo "PR-5.4 -> PDF Text Extraction Pipeline"

echo

echo "Terminal remains open"

