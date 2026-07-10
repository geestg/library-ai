import json
import uuid

from qdrant_client.models import (
    PointStruct
)

from app.rag.qdrant_client import (
    client,
    ensure_collection_exists
)

from app.core.constants import (
    USER_DOCUMENT_COLLECTION
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

    ensure_collection_exists(
        USER_DOCUMENT_COLLECTION
    )

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

        text = f"""
        Judul:
        {title}

        Abstrak:
        {abstract}
        """

        embedding = get_embedding(
            text
        )

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

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload=payload
        )

        points.append(point)

    client.upsert(

        collection_name=
        USER_DOCUMENT_COLLECTION,

        points=points
    )

    print(
        f"[INGEST] Dataset success: "
        f"{len(points)} indexed."
    )


# =====================================
# INGEST PDF
# =====================================

def ingest_pdf(

    pdf_path,

    session_id: str,

    document_id: str,

    title="Untitled PDF",

    author="Unknown",

    year="2025"
):

    ensure_collection_exists(
        USER_DOCUMENT_COLLECTION
    )

    # =================================
    # EXTRACT PAGES
    # =================================

    pages = extract_pdf_pages(
        pdf_path
    )

    print(
        f"[PDF] Extracted pages: "
        f"{len(pages)}"
    )

    # =================================
    # CHUNKING
    # =================================

    chunks = chunk_text(
        pages
    )

    print(
        f"[CHUNK] Generated chunks: "
        f"{len(chunks)}"
    )

    # =================================
    # BUILD VECTOR POINTS
    # =================================

    points = []

    for chunk in chunks:

        embedding = get_embedding(
            chunk["text"]
        )

        metadata = chunk.get(
            "metadata",
            {}
        )

        payload = {

            # =================================
            # OWNERSHIP
            # =================================

            "session_id": session_id,

            "document_id": document_id,

            "source_type": "user_document",

            # =================================
            # DOCUMENT METADATA
            # =================================

            "title": title,

            "author": author,

            "year": year,

            "text": chunk["text"],

            "abstract": chunk["text"],

            "source_file": pdf_path,

            **metadata
        }

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload=payload
        )

        points.append(point)

    # =================================
    # UPSERT TO QDRANT
    # =================================

    client.upsert(

        collection_name=
        USER_DOCUMENT_COLLECTION,

        points=points
    )

    print(
        f"[INGEST] PDF success: "
        f"{len(points)} chunks indexed."
    )

    # =================================
    # BUILD FULL DOCUMENT TEXT
    # =================================

    full_text = "\n\n".join(

        page["text"]

        for page in pages

        if page.get("text")
    )

    # =================================
    # RETURN DOCUMENT INFO
    # =================================

    return {

        "pages":
        len(pages),

        "chunks":
        len(chunks),

        "full_text":
        full_text,

        # penting untuk retriever
        # dan citation halaman
        "pages_data":
        pages

    }


