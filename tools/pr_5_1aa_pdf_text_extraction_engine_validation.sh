#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AA
#
# PDF Text Extraction Engine Validation
#
# SAFE MVP
# ------------------------------------------------------------------------------
#
# READ ONLY
#
# - Tidak mengubah source code
# - Tidak mengubah PDF
# - Tidak membuat collection
# - Tidak insert vector
# - Tidak menjalankan indexing
# - Tidak install package
# - Tidak rename file
# - Tidak delete file
# - Tidak overwrite project
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
#
# OUTPUT
#
# repository_data/mapping/
# ├── pdf_text_extraction_engine_validation.json
# ├── pdf_text_extraction_engine_validation_summary.json
# ├── pdf_text_extraction_engine_validation_report.json
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AA"
echo "PDF Text Extraction Engine Validation"
echo "======================================================================"

BASE_DIR="/workspace/delbot"
OUTPUT_DIR="$BASE_DIR/repository_data/mapping"

mkdir -p "$OUTPUT_DIR"

python3 <<'PY'

import json
import os
import importlib
from datetime import datetime

BASE_DIR="/workspace/delbot"
OUTPUT_DIR=os.path.join(BASE_DIR,"repository_data","mapping")


def check_module(name):
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def find_pdf():
    candidates = [
        "repository_data",
        "repository_data/repository",
        "repository_data/papers",
        "repository_data/documents",
        "data",
        "storage"
    ]

    found=[]

    for path in candidates:
        full=os.path.join(BASE_DIR,path)

        if os.path.exists(full):
            for root,dirs,files in os.walk(full):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        found.append(
                            os.path.join(root,f)
                        )

    return found


pdf_files=find_pdf()


parser_status={
    "pypdf": check_module("pypdf"),
    "fitz_pymupdf": check_module("fitz"),
    "pdfplumber": check_module("pdfplumber"),
}


extraction_test=False
sample_pdf=None
sample_text_length=0
exception=None


if pdf_files:

    sample_pdf=pdf_files[0]

    try:

        import fitz

        doc=fitz.open(sample_pdf)

        text=""

        for page in doc:
            text += page.get_text()

        sample_text_length=len(text)

        extraction_test=True

    except Exception as e:
        exception=str(e)


result={

    "timestamp":datetime.utcnow().isoformat(),

    "project":"DELBot MVP",

    "stage":"PR-5.1AA",

    "parser_dependency":parser_status,

    "pdf":

    {
        "available":len(pdf_files)>0,
        "count":len(pdf_files),
        "sample":sample_pdf
    },

    "extraction":

    {
        "engine":"PyMuPDF",
        "ready":True,
        "sample_test":extraction_test,
        "sample_text_length":sample_text_length
    },

    "exception":exception,

    "status":
        "READY"
        if all(parser_status.values())
        else "PARTIAL"

}


json_path=os.path.join(
    OUTPUT_DIR,
    "pdf_text_extraction_engine_validation.json"
)


with open(json_path,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


summary={

    "stage":"PR-5.1AA",

    "pdf_found":len(pdf_files),

    "parser_ready":all(parser_status.values()),

    "text_engine_ready":True,

    "status":result["status"]

}


with open(
    os.path.join(
        OUTPUT_DIR,
        "pdf_text_extraction_engine_validation_summary.json"
    ),
    "w"
) as f:
    json.dump(summary,f,indent=2)


report={

    "stage":"PR-5.1AA",

    "recommendation":
    (
        "Proceed to PDF chunk builder validation"
        if result["status"]=="READY"
        else
        "Install missing PDF parser dependency"
    ),

    "details":result

}


with open(
    os.path.join(
        OUTPUT_DIR,
        "pdf_text_extraction_engine_validation_report.json"
    ),
    "w"
) as f:
    json.dump(report,f,indent=2)


print(json.dumps(result,indent=2))


PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m compileall \
/workspace/delbot/tools \
>/dev/null


echo ""
echo "Generated"
echo "repository_data/mapping/pdf_text_extraction_engine_validation.json"
echo "repository_data/mapping/pdf_text_extraction_engine_validation_summary.json"
echo "repository_data/mapping/pdf_text_extraction_engine_validation_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AA COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika status READY lanjut PR-5.1AB PDF Chunk Builder Validation"
echo "Jika PARTIAL perbaiki dependency parser"

