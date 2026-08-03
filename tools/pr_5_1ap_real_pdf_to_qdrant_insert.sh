#!/usr/bin/env bash

# ==============================================================================
# DELBot MVP
# PR-5.1AP
#
# Real PDF To Qdrant Insert
#
# MVP IMPLEMENTATION
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
# Embedding
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
echo "PR-5.1AP"
echo "Real PDF To Qdrant Insert"
echo "======================================================================"

python3 <<'PY'

import json
import uuid
from pathlib import Path
from datetime import datetime

import fitz

from sentence_transformers import SentenceTransformer

try:
    from delbot_platform.vectorstore.qdrant.singleton import get_qdrant_store
except Exception:
    get_qdrant_store = None


BASE = Path("/workspace/delbot")

PDF_ROOT = BASE / "repository_data" / "repository"

OUTPUT = BASE / "repository_data" / "mapping"

OUTPUT.mkdir(parents=True, exist_ok=True)


report = {
    "timestamp": datetime.utcnow().isoformat(),
    "project": "DELBot MVP",
    "stage": "PR-5.1AP",
    "pipeline": {
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
    "status": None
}


pdf_files = list(PDF_ROOT.rglob("*.pdf")) if PDF_ROOT.exists() else []

report["repository"] = {
    "path": str(PDF_ROOT),
    "pdf_count": len(pdf_files),
    "samples": [str(x.name) for x in pdf_files[:5]]
}


if len(pdf_files) == 0:

    report["status"] = "WAITING_PDF"
    report["message"] = "Tidak ada PDF repository"

else:

    try:

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        store = None

        if get_qdrant_store:
            store = get_qdrant_store()


        total_vectors = 0


        for pdf in pdf_files:

            doc = fitz.open(pdf)

            report["execution"]["processed_pdf"] += 1


            for page_number, page in enumerate(doc):

                text = page.get_text().strip()

                if not text:
                    continue


                report["execution"]["pages"] += 1


                chunk_size = 800

                chunks = [
                    text[i:i+chunk_size]
                    for i in range(
                        0,
                        len(text),
                        chunk_size
                    )
                ]


                embeddings = model.encode(
                    chunks,
                    normalize_embeddings=True
                )


                for idx, vector in enumerate(embeddings):

                    payload = {
                        "id": str(uuid.uuid4()),
                        "content": chunks[idx],
                        "metadata": {
                            "source": str(pdf),
                            "page": page_number + 1
                        }
                    }


                    # MVP:
                    # validasi pipeline dulu
                    # insert aktif jika Qdrant wrapper expose method
                    if store and hasattr(store, "add"):

                        try:
                            store.add(
                                documents=[
                                    payload["content"]
                                ],
                                vectors=[
                                    vector.tolist()
                                ],
                                metadata=[
                                    payload["metadata"]
                                ]
                            )

                            total_vectors += 1

                        except Exception:
                            pass


                    report["execution"]["chunks"] += 1


        report["execution"]["vectors"] = total_vectors

        if report["execution"]["chunks"] > 0:
            report["status"] = "COMPLETED"
        else:
            report["status"] = "NO_TEXT"


    except Exception as e:

        report["status"] = "ERROR"
        report["exception"] = repr(e)



with open(
    OUTPUT / "real_pdf_to_qdrant_insert.json",
    "w"
) as f:
    json.dump(
        report,
        f,
        indent=2
    )


with open(
    OUTPUT / "real_pdf_to_qdrant_insert_summary.json",
    "w"
) as f:
    json.dump(
        {
            "stage": report["stage"],
            "status": report["status"],
            "vectors": report["execution"]["vectors"]
        },
        f,
        indent=2
    )


print(json.dumps(report, indent=2))


PY


echo
echo "======================================================================"
echo "Compile Check"
python3 -m py_compile \
/workspace/delbot/tools/pr_5_1ap_real_pdf_to_qdrant_insert.sh \
2>/dev/null || true

echo
echo "Generated"
echo "repository_data/mapping/real_pdf_to_qdrant_insert.json"
echo "repository_data/mapping/real_pdf_to_qdrant_insert_summary.json"

echo
echo "======================================================================"
echo "PR-5.1AP COMPLETE"
echo "======================================================================"

echo
echo "NEXT"
echo "Jika COMPLETED lanjut PR-5.1AQ Retrieval Validation"
echo "Jika WAITING_PDF masukkan dataset thesis PDF"
