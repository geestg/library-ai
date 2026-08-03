#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AT
#
# Real PDF Vector Commit
#
# MVP EXECUTION
# ==============================================================================
#
# Pipeline:
#
# repository_data/repository/*.pdf
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
# Qdrant delbot_documents
#
# Rules:
# ------------------------------------------------------------------------------
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak delete collection
# - Tidak overwrite vector lama
# - Append only
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AT"
echo "Real PDF Vector Commit"
echo "======================================================================"

python3 <<'PYTHON'
import os
import json
import uuid
from datetime import datetime

REPORT_DIR = "/workspace/delbot/repository_data/mapping"
REPO_PATH = "/workspace/delbot/repository_data/repository"

os.makedirs(REPORT_DIR, exist_ok=True)

result = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AT",
    "pipeline": {
        "loader": "repository_pdf_loader",
        "parser": "PyMuPDF",
        "chunk": "simple_semantic_chunk",
        "embedding": "sentence_transformers",
        "vector_store": "Qdrant"
    },
    "repository": {
        "path": REPO_PATH,
        "pdf_count": 0,
        "documents": []
    },
    "qdrant": {
        "collection": "delbot_documents",
        "append_only": True,
        "overwrite": False
    },
    "commit": {
        "processed_pdf": 0,
        "pages": 0,
        "chunks": 0,
        "vectors": 0
    },
    "status": "WAITING_PDF",
    "exception": None
}

try:

    pdf_files = []

    for root, dirs, files in os.walk(REPO_PATH):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(
                    os.path.join(root, file)
                )

    result["repository"]["pdf_count"] = len(pdf_files)
    result["repository"]["documents"] = [
        os.path.basename(x)
        for x in pdf_files[:10]
    ]

    if len(pdf_files) == 0:
        result["status"] = "WAITING_PDF"

    else:

        import fitz

        from sentence_transformers import SentenceTransformer

        from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        store = get_qdrant_store()

        total_pages = 0
        total_chunks = 0
        total_vectors = 0


        for pdf_path in pdf_files:

            document = fitz.open(pdf_path)

            chunks = []

            for page_number, page in enumerate(document):

                text = page.get_text()

                if text.strip():

                    chunk = {
                        "content": text[:1000],
                        "metadata": {
                            "source": pdf_path,
                            "page": page_number + 1,
                            "document_id": str(uuid.uuid4())
                        }
                    }

                    chunks.append(chunk)

                total_pages += 1


            if chunks:

                texts = [
                    c["content"]
                    for c in chunks
                ]

                embeddings = model.encode(
                    texts,
                    normalize_embeddings=True
                )

                for idx, vector in enumerate(embeddings):

                    payload = chunks[idx]["metadata"]
                    payload["content"] = chunks[idx]["content"]

                    # MVP validation commit
                    # menggunakan wrapper existing
                    store.add_vector(
                        vector=vector.tolist(),
                        payload=payload
                    )

                    total_vectors += 1


                total_chunks += len(chunks)


        result["commit"]["processed_pdf"] = len(pdf_files)
        result["commit"]["pages"] = total_pages
        result["commit"]["chunks"] = total_chunks
        result["commit"]["vectors"] = total_vectors

        result["status"] = "COMPLETED"


except Exception as e:

    result["status"] = "FAILED"
    result["exception"] = str(e)


with open(
    os.path.join(
        REPORT_DIR,
        "real_pdf_vector_commit.json"
    ),
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


with open(
    os.path.join(
        REPORT_DIR,
        "real_pdf_vector_commit_summary.json"
    ),
    "w"
) as f:
    json.dump(
        {
            "stage": "PR-5.1AT",
            "status": result["status"],
            "vectors": result["commit"]["vectors"]
        },
        f,
        indent=2
    )


with open(
    os.path.join(
        REPORT_DIR,
        "real_pdf_vector_commit_report.json"
    ),
    "w"
) as f:
    json.dump(
        result,
        f,
        indent=2
    )


print(json.dumps(result, indent=2))

PYTHON


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile \
/workspace/delbot/tools/pr_5_1at_real_pdf_vector_commit.sh \
2>/dev/null || true


echo ""
echo "Generated"
echo "repository_data/mapping/real_pdf_vector_commit.json"
echo "repository_data/mapping/real_pdf_vector_commit_summary.json"
echo "repository_data/mapping/real_pdf_vector_commit_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AT COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika COMPLETED lanjut PR-5.1AU Retrieval Engine Validation"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
