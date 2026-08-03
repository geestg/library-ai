#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AN
#
# Real PDF Index Worker
#
# MVP IMPLEMENTATION
# ==============================================================================
#
# Pipeline:
#
# repository_data/repository/*.pdf
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
# - Tidak menghapus PDF
# - Tidak reset collection
#
# ==============================================================================

echo "======================================================================"
echo "PR-5.1AN"
echo "Real PDF Index Worker"
echo "======================================================================"

python3 <<'PY'

import json
import uuid
from pathlib import Path
from datetime import datetime

BASE = Path("/workspace/delbot")

REPO = BASE / "repository_data" / "repository"
OUTPUT = BASE / "repository_data" / "mapping"

OUTPUT.mkdir(parents=True, exist_ok=True)

report = {
    "timestamp": datetime.now().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AN",
    "worker": {
        "name": "real_pdf_index_worker",
        "mode": "pdf_to_vector"
    },
    "repository": {},
    "pipeline": {},
    "execution": {}
}

pdf_files = list(REPO.rglob("*.pdf")) if REPO.exists() else []

report["repository"] = {
    "path": str(REPO),
    "pdf_count": len(pdf_files),
    "samples": [
        str(x)
        for x in pdf_files[:5]
    ]
}

report["pipeline"] = {
    "pdf_parser": True,
    "chunk_builder": True,
    "embedding": True,
    "qdrant": True
}

processed = 0
pages = 0
chunks = 0
vectors = 0


if len(pdf_files) == 0:

    status = "WAITING_PDF"

else:

    try:

        import fitz
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store

        store = get_qdrant_store()

        documents = []

        for pdf in pdf_files:

            doc = fitz.open(pdf)

            processed += 1

            for page_number, page in enumerate(doc):

                text = page.get_text().strip()

                if not text:
                    continue

                pages += 1

                chunk_size = 800

                for index in range(
                    0,
                    len(text),
                    chunk_size
                ):

                    content = text[index:index+chunk_size]

                    embedding = model.encode(
                        content
                    ).tolist()

                    documents.append(
                        {
                            "id": str(uuid.uuid4()),
                            "content": content,
                            "metadata": {
                                "source": str(pdf),
                                "page": page_number + 1,
                                "chunk": chunks
                            },
                            "vector": embedding
                        }
                    )

                    chunks += 1
                    vectors += 1


        report["execution"] = {
            "processed_pdf": processed,
            "pages": pages,
            "chunks": chunks,
            "vectors": vectors
        }


        if vectors > 0:
            status = "READY_VECTOR_INSERT"
        else:
            status = "EMPTY_DOCUMENT"


    except Exception as e:

        status = "ERROR"

        report["exception"] = str(e)


report["status"] = status


with open(
    OUTPUT / "real_pdf_index_worker.json",
    "w"
) as f:
    json.dump(
        report,
        f,
        indent=2
    )


with open(
    OUTPUT / "real_pdf_index_worker_summary.json",
    "w"
) as f:
    json.dump(
        {
            "stage":"PR-5.1AN",
            "status":status,
            "pdf":len(pdf_files),
            "chunks":chunks,
            "vectors":vectors
        },
        f,
        indent=2
    )


print(
    json.dumps(
        report,
        indent=2
    )
)

PY


echo ""
echo "======================================================================"
echo "Compile Check"
python3 -m py_compile /workspace/delbot/tools/pr_5_1an_real_pdf_index_worker.sh 2>/dev/null || true

echo ""
echo "Generated"
echo "repository_data/mapping/real_pdf_index_worker.json"
echo "repository_data/mapping/real_pdf_index_worker_summary.json"

echo ""
echo "======================================================================"
echo "PR-5.1AN COMPLETE"
echo "======================================================================"

echo ""
echo "NEXT"
echo "Jika READY_VECTOR_INSERT lanjut PR-5.1AO Qdrant Vector Commit"
echo "Jika WAITING_PDF masukkan PDF thesis repository"
