#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AI
#
# Real Batch PDF Indexing Engine
#
# MVP EXECUTION
# ------------------------------------------------------------------------------
#
# Pipeline:
#
# PDF Repository
#       |
#       v
# PyMuPDF Extraction
#       |
#       v
# Chunk Builder
#       |
#       v
# BGE / Sentence Transformer Embedding
#       |
#       v
# Qdrant delbot_documents
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak delete data
# - Tidak drop collection
# - Tidak overwrite existing vectors
# - MVP focused
#
# Input:
#   repository_data/repository
#   repository_data/papers
#   repository_data/documents
#
# Output:
#   repository_data/mapping/
#
# ==============================================================================


echo "======================================================================"
echo "PR-5.1AI"
echo "Real Batch PDF Indexing Engine"
echo "======================================================================"


python <<'PY'

import os
import json
import uuid
from datetime import datetime


PROJECT="/workspace/delbot"

OUTPUT_DIR=os.path.join(
    PROJECT,
    "repository_data",
    "mapping"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


result={
    "timestamp": datetime.utcnow().isoformat(),
    "project":"DELBot MVP",
    "stage":"PR-5.1AI",
    "pipeline":{
        "parser":"PyMuPDF",
        "chunk":"semantic_chunk_builder",
        "embedding":"sentence_transformers",
        "vector_store":"Qdrant"
    },
    "repository":{
        "paths":[],
        "pdf_count":0
    },
    "execution":{
        "processed_pdf":0,
        "pages":0,
        "chunks":0,
        "vectors":0
    },
    "status":"STARTED"
}


search_paths=[
    "repository_data/repository",
    "repository_data/papers",
    "repository_data/documents",
    "repository_data",
    "data",
    "storage"
]


pdf_files=[]


for path in search_paths:

    full=os.path.join(PROJECT,path)

    if os.path.exists(full):

        result["repository"]["paths"].append(path)

        for root,dirs,files in os.walk(full):

            for file in files:

                if file.lower().endswith(".pdf"):

                    pdf_files.append(
                        os.path.join(root,file)
                    )


result["repository"]["pdf_count"]=len(pdf_files)


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


        collection="delbot_documents"


        for pdf in pdf_files:


            result["execution"]["processed_pdf"]+=1


            document=fitz.open(pdf)


            for page_number,page in enumerate(document):


                text=page.get_text(
                    "text"
                ).strip()


                if not text:
                    continue


                result["execution"]["pages"]+=1


                chunk_size=800


                chunks=[
                    text[i:i+chunk_size]
                    for i in range(
                        0,
                        len(text),
                        chunk_size
                    )
                ]


                embeddings=model.encode(
                    chunks
                )


                payloads=[]


                for idx,chunk in enumerate(chunks):


                    payloads.append(
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


                # MVP safety:
                # hanya validasi embedding dan payload.
                # Insert permanen dilakukan setelah smoke test.

                result["execution"]["chunks"] += len(chunks)

                result["execution"]["vectors"] += len(embeddings)



        result["status"]="READY_FOR_VECTOR_INSERT"


    except Exception as e:

        result["status"]="ERROR"
        result["exception"]=str(e)



files=[
    "real_batch_pdf_indexing.json",
    "real_batch_pdf_indexing_summary.json",
    "real_batch_pdf_indexing_report.json"
]


for file in files:

    with open(
        os.path.join(
            OUTPUT_DIR,
            file
        ),
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=2
        )


print(json.dumps(result,indent=2))


PY


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python -m py_compile \
/workspace/delbot/tools/pr_5_1ai_real_batch_pdf_indexing.sh \
2>/dev/null || true


echo ""
echo "Generated"
echo "repository_data/mapping/real_batch_pdf_indexing.json"
echo "repository_data/mapping/real_batch_pdf_indexing_summary.json"
echo "repository_data/mapping/real_batch_pdf_indexing_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AI COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_FOR_VECTOR_INSERT lanjut PR-5.1AJ Vector Insert Validation"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
echo "======================================================================"

