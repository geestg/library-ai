#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.2
#
# PDF Repository Mapper
#
# MVP SAFE
# ==============================================================================
#
# Purpose:
# Create PDF repository manifest
#
# Tidak melakukan:
# - delete
# - migration
# - rebuild index
# - restart service
#
# Terminal tetap terbuka
#

set -u

ROOT="/workspace/delbot"

PDF_DIR="$ROOT/delbot_platform/repository_data/pdf"

OUTPUT="$ROOT/repository_data/mapping/pdf_repository_manifest.json"


mkdir -p "$(dirname "$OUTPUT")"


echo "======================================================================"
echo "DELBot MVP"
echo "PR-5.2 PDF Repository Mapper"
echo "======================================================================"


python3 <<'PY'

import os
import json
import hashlib
from datetime import datetime


pdf_dir = "/workspace/delbot/delbot_platform/repository_data/pdf"

output = "/workspace/delbot/repository_data/mapping/pdf_repository_manifest.json"


documents = []


def file_hash(path):

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()



if os.path.exists(pdf_dir):

    for filename in sorted(os.listdir(pdf_dir)):

        if filename.lower().endswith(".pdf"):

            path = os.path.join(
                pdf_dir,
                filename
            )

            if os.path.isfile(path):

                stat = os.stat(path)

                documents.append({

                    "document_id":
                        file_hash(path)[:16],

                    "filename":
                        filename,

                    "path":
                        path,

                    "extension":
                        ".pdf",

                    "size_bytes":
                        stat.st_size,

                    "sha256":
                        file_hash(path),

                    "indexed":
                        False

                })



result = {

    "project":
        "DELBot MVP",

    "stage":
        "PR-5.2",

    "timestamp":
        datetime.utcnow().isoformat() + "Z",

    "repository":
    {

        "path":
            pdf_dir,

        "exists":
            os.path.exists(pdf_dir)

    },

    "statistics":
    {

        "total_pdf":
            len(documents)

    },

    "documents":
        documents

}



with open(output, "w") as f:

    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps({

    "status":
        "PDF_MAPPING_COMPLETE",

    "pdf_count":
        len(documents),

    "output":
        output

}, indent=2))


PY


echo

echo "======================================================================"
echo "Generated"
echo "$OUTPUT"
echo "======================================================================"

echo

echo "PR-5.2 COMPLETE"

echo

echo "NEXT"
echo "PR-5.3 -> PDF metadata extraction + parser validation"

echo

echo "Terminal remains open"
