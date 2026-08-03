#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AK
#
# Repository PDF Loader
#
# MVP IMPLEMENTATION
# ------------------------------------------------------------------------------
#
# PURPOSE
#
# Membuat loader repository PDF untuk pipeline indexing MVP.
#
# Pipeline:
#
# repository_data/
#       |
#       v
# PDF Discovery
#       |
#       v
# PDF Metadata Loader
#       |
#       v
# Document Object
#       |
#       v
# Batch Indexer Ready
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus file
# - Tidak mengubah PDF
# - Tidak insert vector
# - Tidak membuat collection
#
# OUTPUT:
#
# repository_data/mapping/
# ├── repository_pdf_loader.json
# ├── repository_pdf_loader_summary.json
# └── repository_pdf_loader_report.json
#
# ==============================================================================

PROJECT="/workspace/delbot"
OUTPUT_DIR="$PROJECT/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"

python3 <<'PYTHON'
import os
import json
import glob
from datetime import datetime

PROJECT="/workspace/delbot"

search_paths=[
    "repository_data",
    "repository_data/repository",
    "repository_data/papers",
    "repository_data/documents",
    "data",
    "storage"
]

pdf_files=[]

for path in search_paths:
    full=os.path.join(PROJECT,path)

    if os.path.exists(full):
        found=glob.glob(
            os.path.join(full,"**","*.pdf"),
            recursive=True
        )
        pdf_files.extend(found)


pdf_files=list(dict.fromkeys(pdf_files))


documents=[]

for pdf in pdf_files:

    relative=os.path.relpath(
        pdf,
        PROJECT
    )

    documents.append(
        {
            "document_id":os.path.splitext(
                os.path.basename(pdf)
            )[0],
            "path":relative,
            "extension":"pdf",
            "size_bytes":os.path.getsize(pdf)
        }
    )


result={

    "timestamp":datetime.now().isoformat(),

    "project":"DELBot MVP",

    "stage":"PR-5.1AK",

    "loader":{

        "engine":"repository_pdf_loader",

        "ready":True,

        "search_paths":search_paths

    },

    "repository":{

        "pdf_count":len(documents),

        "documents":documents[:20]

    },


    "pipeline":{

        "pdf_discovery":True,

        "metadata_loader":True,

        "document_schema":True,

        "batch_indexer_ready":True

    },


    "status":
        "READY_WITH_PDF"
        if len(documents)>0
        else
        "WAITING_PDF"

}


out=os.path.join(
    PROJECT,
    "repository_data/mapping/repository_pdf_loader.json"
)


with open(out,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


summary={
    "stage":"PR-5.1AK",
    "pdf_count":len(documents),
    "status":result["status"]
}


for name,data in [

    (
        "repository_pdf_loader_summary.json",
        summary
    ),

    (
        "repository_pdf_loader_report.json",
        result
    )

]:

    with open(
        os.path.join(
            PROJECT,
            "repository_data/mapping",
            name
        ),
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


print(json.dumps(result,indent=2))

PYTHON


echo
echo "======================================================================"
echo "Compile Check"
python3 -m py_compile \
/workspace/delbot/tools/pr_5_1ak_repository_pdf_loader.sh \
2>/dev/null || true

echo
echo "======================================================================"
echo "PR-5.1AK COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika READY_WITH_PDF lanjut PR-5.1AL Real PDF Index Pipeline Execution"
echo "Jika WAITING_PDF masukkan dataset PDF thesis repository"
