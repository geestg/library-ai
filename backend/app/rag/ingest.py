import json
import uuid

from qdrant_client.models import (
    PointStruct
)

from app.rag.qdrant_client import (
    client,
    COLLECTION_NAME,
    ensure_collection_exists
)

from app.rag.embedder import (
    get_embedding
)

from app.document.parsers.pdf_parser import (
    extract_pdf_pages
)

from app.rag.chunker import (
    chunk_text
)

# =====================================
# INGEST JSON DATASET
# =====================================

def ingest_dataset():

    ensure_collection_exists()

    dataset_path = (
        "/app/datasets/skripsi_dataset.json"
    )

    with open(
        dataset_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    points = []

    # =================================
    # PROCESS ITEMS
    # =================================

    for idx, item in enumerate(data):

        title = item.get(
            "judul",
            ""
        )

        author = item.get(
            "penulis",
            ""
        )

        year = item.get(
            "tahun",
            ""
        )

        abstract = item.get(
            "abstrak",
            ""
        )

        # =============================
        # TEXT FOR EMBEDDING
        # =============================

        text = f"""
        Judul:
        {title}

        Abstrak:
        {abstract}
        """

        # =============================
        # GENERATE EMBEDDING
        # =============================

        embedding = get_embedding(
            text
        )

        # =============================
        # PAYLOAD
        # =============================

        payload = {

            "title": title,

            "author": author,

            "year": year,

            "abstract": abstract,

            "text": text,

            "source_file": item.get(
                "source_file",
                "dataset_ingest.json"
            ),

            "page": item.get(
                "page",
                1
            ),

            "chunk_index": idx
        }

        # =============================
        # BUILD POINT
        # =============================

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload=payload
        )

        points.append(point)

    # =================================
    # UPSERT
    # =================================

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points
    )

    print(
        f"[INGEST] Dataset success: {len(points)} indexed."
    )


# =====================================
# INGEST PDF
# =====================================

def ingest_pdf(

    pdf_path,

    title="Untitled PDF",

    author="Unknown",

    year="2025"
):

    ensure_collection_exists()

    # =================================
    # EXTRACT PDF PAGES
    # =================================

    pages = extract_pdf_pages(
        pdf_path
    )

    print(
        f"[PDF] Extracted pages: {len(pages)}"
    )

    # =================================
    # CHUNKING
    # =================================

    chunks = chunk_text(
        pages
    )

    print(
        f"[CHUNK] Generated chunks: {len(chunks)}"
    )

    # =================================
    # BUILD POINTS
    # =================================

    points = []

    for chunk in chunks:

        # =============================
        # EMBEDDING
        # =============================

        embedding = get_embedding(
            chunk["text"]
        )

        # =============================
        # METADATA
        # =============================

        metadata = chunk.get(
            "metadata",
            {}
        )

        # =============================
        # PAYLOAD
        # =============================

        payload = {

            "title": title,

            "author": author,

            "year": year,

            "text": chunk["text"],

            "abstract": chunk["text"],

            "source_file": pdf_path,

            # =========================
            # CHUNK METADATA
            # =========================

            **metadata
        }

        # =============================
        # BUILD POINT
        # =============================

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload=payload
        )

        points.append(point)

    # =================================
    # UPSERT
    # =================================

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points
    )

    print(
        f"[INGEST] PDF success: {len(points)} chunks indexed."
    )


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    ingest_dataset()