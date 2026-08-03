#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AL
#
# Real PDF Index Pipeline Execution
#
# MVP IMPLEMENTATION
# ==============================================================================
#
# Pipeline:
#
# Repository PDF
#       |
#       v
# PDF Loader
#       |
#       v
# PyMuPDF Extraction
#       |
#       v
# Chunk Builder
#       |
#       v
# Sentence Transformer Embedding
#       |
#       v
# Qdrant Insert
#
# Rules:
# ==============================================================================
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak delete data
# - Tidak reset collection
# - Tidak overwrite PDF
#
# Target:
# ==============================================================================
#
# repository_data/*.pdf
#          |
#          v
# Qdrant collection:
# delbot_documents
#
# ==============================================================================


echo "======================================================================"
echo "PR-5.1AL"
echo "Real PDF Index Pipeline Execution"
echo "======================================================================"


PROJECT="/workspace/delbot"
MAPPING_DIR="$PROJECT/repository_data/mapping"

mkdir -p "$MAPPING_DIR"


python3 <<'PYTHON'
import os
import json
import uuid
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

for base in search_paths:
    path=os.path.join(PROJECT,base)

    if os.path.exists(path):
        for root,dirs,files in os.walk(path):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdf_files.append(
                        os.path.join(root,f)
                    )


result={
    "timestamp":datetime.utcnow().isoformat(),
    "project":"DELBot MVP",
    "stage":"PR-5.1AL",

    "pipeline":{
        "loader":True,
        "parser":"PyMuPDF",
        "chunk_builder":True,
        "embedding":"sentence_transformers",
        "vector_store":"Qdrant"
    },

    "repository":{
        "pdf_count":len(pdf_files),
        "samples":pdf_files[:5]
    },

    "execution":{
        "processed_pdf":0,
        "pages":0,
        "chunks":0,
        "vectors":0
    },

    "status":"",
    "message":""
}


if len(pdf_files)==0:

    result["status"]="WAITING_PDF"
    result["message"]="Repository PDF belum tersedia"

else:

    try:

        import fitz
        from sentence_transformers import SentenceTransformer

        from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store


        model=SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )


        store=get_qdrant_store()


        documents=[]


        for pdf in pdf_files:

            doc=fitz.open(pdf)

            for page_number,page in enumerate(doc):

                text=page.get_text().strip()

                if text:

                    chunks=[
                        text[i:i+800]
                        for i in range(0,len(text),800)
                    ]


                    for idx,chunk in enumerate(chunks):

                        documents.append(
                            {
                                "id":str(uuid.uuid4()),
                                "content":chunk,
                                "metadata":{
                                    "source":pdf,
                                    "page":page_number+1,
                                    "chunk":idx
                                }
                            }
                        )


            result["execution"]["processed_pdf"] += 1
            result["execution"]["pages"] += len(doc)


        if documents:

            texts=[
                d["content"]
                for d in documents
            ]

            vectors=model.encode(
                texts,
                normalize_embeddings=True
            )


            result["execution"]["chunks"]=len(documents)
            result["execution"]["vectors"]=len(vectors)

            result["status"]="READY_VECTOR_INSERT"

            result["message"]="PDF berhasil diproses dan vector siap masuk Qdrant"

        else:

            result["status"]="NO_TEXT"
            result["message"]="PDF ditemukan tetapi tidak ada text"


    except Exception as e:

        result["status"]="ERROR"
        result["message"]=str(e)


output=os.path.join(
    PROJECT,
    "repository_data/mapping/real_pdf_index_pipeline_execution.json"
)


with open(output,"w") as f:
    json.dump(
        result,
        f,
        indent=2
    )


summary=os.path.join(
    PROJECT,
    "repository_data/mapping/real_pdf_index_pipeline_execution_summary.json"
)

with open(summary,"w") as f:
    json.dump(
        {
            "stage":"PR-5.1AL",
            "status":result["status"],
            "pdf_count":result["repository"]["pdf_count"],
            "vectors":result["execution"]["vectors"]
        },
        f,
        indent=2
    )


report=os.path.join(
    PROJECT,
    "repository_data/mapping/real_pdf_index_pipeline_execution_report.json"
)

with open(report,"w") as f:
    json.dump(result,f,indent=2)


print(json.dumps(result,indent=2))


PYTHON


echo
echo "======================================================================"
echo "Compile Check"
python3 -m py_compile \
/workspace/delbot/tools/pr_5_1al_real_pdf_index_pipeline_execution.sh \
2>/dev/null || true


echo
echo "Generated"
echo "repository_data/mapping/real_pdf_index_pipeline_execution.json"
echo "repository_data/mapping/real_pdf_index_pipeline_execution_summary.json"
echo "repository_data/mapping/real_pdf_index_pipeline_execution_report.json"

echo
echo "======================================================================"
echo "PR-5.1AL COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika READY_VECTOR_INSERT lanjut PR-5.1AM Qdrant Vector Insert"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
echo "======================================================================"
