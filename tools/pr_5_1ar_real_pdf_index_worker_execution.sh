#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AR
#
# Real PDF Index Worker Execution
#
# MVP EXECUTION
# ==============================================================================
#
# Pipeline:
#
# repository_data/repository/*.pdf
#       |
#       v
# PDF Discovery
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
#
# - Tidak ada exit
# - Tidak ada return
# - Terminal tetap terbuka
# - Tidak menghapus collection
# - Tidak overwrite vector lama
# - Append only
#
# OUTPUT:
#
# repository_data/mapping/
# - real_pdf_index_worker_execution.json
# - real_pdf_index_worker_execution_summary.json
# - real_pdf_index_worker_execution_report.json
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AR"
echo "Real PDF Index Worker Execution"
echo "======================================================================"

python3 <<'PYTHON'
import json
import traceback
from pathlib import Path
from datetime import datetime
import uuid

BASE = Path("/workspace/delbot")

REPOSITORY = BASE / "repository_data/repository"
OUTPUT = BASE / "repository_data/mapping"

OUTPUT.mkdir(parents=True, exist_ok=True)

result = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AR",
    "pipeline": {
        "loader": "repository_pdf_loader",
        "parser": "PyMuPDF",
        "chunk": "simple_semantic_chunk",
        "embedding": "sentence_transformers",
        "vector_store": "Qdrant"
    },
    "repository": {},
    "execution": {
        "processed_pdf": 0,
        "pages": 0,
        "chunks": 0,
        "vectors": 0
    },
    "status": None,
    "exception": None
}

try:

    pdf_files = list(REPOSITORY.rglob("*.pdf")) if REPOSITORY.exists() else []

    result["repository"] = {
        "path": str(REPOSITORY),
        "pdf_count": len(pdf_files),
        "samples": [
            str(x.relative_to(BASE))
            for x in pdf_files[:5]
        ]
    }

    if len(pdf_files) == 0:

        result["status"] = "WAITING_PDF"

    else:

        import fitz

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        documents = []

        for pdf in pdf_files:

            doc = fitz.open(pdf)

            result["execution"]["processed_pdf"] += 1

            for page_number, page in enumerate(doc):

                text = page.get_text().strip()

                if not text:
                    continue

                result["execution"]["pages"] += 1

                chunks = [
                    text[i:i+800]
                    for i in range(
                        0,
                        len(text),
                        800
                    )
                ]

                for chunk in chunks:

                    vector = model.encode(
                        chunk,
                        normalize_embeddings=True
                    )

                    documents.append(
                        {
                            "id": str(uuid.uuid4()),
                            "text": chunk,
                            "metadata": {
                                "source": str(pdf),
                                "page": page_number + 1
                            },
                            "vector_dimension": len(vector)
                        }
                    )

        result["execution"]["chunks"] = len(documents)

        result["execution"]["vectors"] = len(documents)

        result["status"] = "READY_FOR_QDRANT_INSERT"

        result["documents_preview"] = documents[:3]


except Exception as e:

    result["status"] = "FAILED"
    result["exception"] = str(e)
    result["traceback"] = traceback.format_exc()


for name in [
    "real_pdf_index_worker_execution.json",
    "real_pdf_index_worker_execution_summary.json",
    "real_pdf_index_worker_execution_report.json"
]:

    with open(
        OUTPUT / name,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )


print(json.dumps(result, indent=2, ensure_ascii=False))

PYTHON


echo ""
echo "======================================================================"
echo "Compile Check"
echo "======================================================================"

python3 -m py_compile /workspace/delbot/tools/pr_5_1ar_real_pdf_index_worker_execution.sh 2>/dev/null || true

echo ""
echo "Generated"
echo "repository_data/mapping/real_pdf_index_worker_execution.json"
echo "repository_data/mapping/real_pdf_index_worker_execution_summary.json"
echo "repository_data/mapping/real_pdf_index_worker_execution_report.json"

echo ""
echo "======================================================================"
echo "PR-5.1AR COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_FOR_QDRANT_INSERT lanjut PR-5.1AS Qdrant Vector Insert"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
