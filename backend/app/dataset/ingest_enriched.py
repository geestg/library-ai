"""
INGEST ENRICHED THESIS DATASET
================================
Membaca skripsi_dataset_enriched.json dan mengupload semua chunk
ke Qdrant collection 'thesis_dataset' menggunakan Ollama nomic-embed-text.

Setiap skripsi menghasilkan beberapa chunk dari:
  - Abstract
  - Bab 1 (Pendahuluan)
  - Bab 3 (Metodologi)
  - Bab 5 (Kesimpulan/Saran)

Setiap chunk menyimpan metadata lengkap:
  - title, author, year, prodi, url, keywords, source_bab

Jalankan dari dalam container:
  docker exec libraryai_backend python app/dataset/ingest_enriched.py
"""

import json
import re
import uuid

from qdrant_client.models import PointStruct

from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client, ensure_collection_exists
from app.core.constants import THESIS_DATASET_COLLECTION


# =========================================
# CONFIG
# =========================================

DATASET_PATH = "/app/app/dataset/skripsi_dataset_enriched.json"
CHUNK_SIZE   = 800    # characters per chunk (tuned for nomic-embed-text 2048 token limit)
CHUNK_OVERLAP = 100   # overlap between chunks
BATCH_SIZE   = 32     # upsert batch to Qdrant

# Prodi normalization: MI D3 aligned with Informatika & TRPL
PRODI_ALIASES = {
    "MI D3": "Informatika",
    "Manajemen Informatika": "Informatika",
}


# =========================================
# CLEAN TEXT
# =========================================

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\r\n", " ", text)
    text = re.sub(r"\n+",  " ", text)
    text = re.sub(r"\s+",  " ", text)
    return text.strip()


# =========================================
# CHUNKER
# =========================================

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping character-level chunks."""
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


# =========================================
# BUILD CHUNKS FROM ONE THESIS ITEM
# =========================================

def build_chunks(item: dict) -> list:
    """
    Given one enriched thesis record, produce a list of
    (chunk_text, source_bab, chunk_index) tuples.
    """
    title    = clean_text(item.get("title",  ""))
    author   = clean_text(item.get("author", ""))
    year     = item.get("year",  "")
    prodi    = item.get("prodi", "")
    url      = item.get("url",   "")
    keywords = item.get("keywords", [])
    content  = item.get("content", {})

    # Normalise prodi
    prodi = PRODI_ALIASES.get(prodi, prodi)

    base_payload = {
        "title"   : title,
        "author"  : author,
        "year"    : year,
        "prodi"   : prodi,
        "url"     : url,
        "keywords": keywords,
    }

    all_chunks = []

    # --- Abstract (always present) ---
    abstract = clean_text(content.get("abstract", ""))
    if not abstract:
        abstract = clean_text(item.get("abstract", ""))

    if abstract:
        # Abstract is short, treat as single chunk prefixed with title
        text = f"Judul: {title}\nAbstrak: {abstract}"
        all_chunks.append({
            **base_payload,
            "source_bab": "abstract",
            "chunk": clean_text(text),
        })

    # --- Bab 1, 3, 5 ---
    bab_map = {
        "bab1": "Bab 1 - Pendahuluan",
        "bab3": "Bab 3 - Metodologi",
        "bab5": "Bab 5 - Kesimpulan",
    }

    for bab_key, bab_label in bab_map.items():
        bab_text = clean_text(content.get(bab_key, ""))
        if not bab_text:
            continue

        sub_chunks = chunk_text(bab_text)
        for idx, sub in enumerate(sub_chunks):
            all_chunks.append({
                **base_payload,
                "source_bab"  : bab_key,
                "source_label": bab_label,
                "chunk_index" : idx,
                "chunk"       : sub,
            })

    return all_chunks


# =========================================
# INGEST
# =========================================

def ingest_enriched():

    print("\n" + "="*60)
    print("INGEST ENRICHED THESIS DATASET")
    print("="*60)

    # Ensure Qdrant collection exists (768-dim nomic-embed-text)
    ensure_collection_exists(THESIS_DATASET_COLLECTION)

    # Load enriched dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"[LOAD] {len(dataset)} thesis records loaded")

    # Build all chunk dicts
    all_chunk_dicts = []
    for item in dataset:
        all_chunk_dicts.extend(build_chunks(item))

    print(f"[CHUNK] {len(all_chunk_dicts)} total chunks generated")

    if not all_chunk_dicts:
        print("[ERROR] No chunks generated. Exiting.")
        return

    # Embed + upsert in batches
    points_buffer = []
    errors        = 0
    success       = 0

    for i, chunk_dict in enumerate(all_chunk_dicts):

        chunk_text_val = chunk_dict["chunk"]

        if not chunk_text_val:
            continue

        try:
            vector = get_embedding(chunk_text_val)

            point = PointStruct(
                id      = str(uuid.uuid4()),
                vector  = vector,
                payload = chunk_dict,
            )
            points_buffer.append(point)
            success += 1

        except Exception as e:
            errors += 1
            print(f"[EMBED ERROR] chunk {i}: {str(e)}")
            continue

        # Upsert when buffer reaches BATCH_SIZE
        if len(points_buffer) >= BATCH_SIZE:
            try:
                client.upsert(
                    collection_name=THESIS_DATASET_COLLECTION,
                    points=points_buffer,
                )
                print(
                    f"[UPSERT] {success} embedded | "
                    f"{errors} errors | "
                    f"batch {i // BATCH_SIZE}"
                )
            except Exception as e:
                print(f"[QDRANT ERROR] {str(e)}")
            points_buffer = []

    # Flush remaining
    if points_buffer:
        try:
            client.upsert(
                collection_name=THESIS_DATASET_COLLECTION,
                points=points_buffer,
            )
        except Exception as e:
            print(f"[QDRANT FLUSH ERROR] {str(e)}")

    print("\n" + "="*60)
    print("INGESTION COMPLETE")
    print(f"  Total chunks embedded : {success}")
    print(f"  Total errors          : {errors}")
    print("="*60)


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    ingest_enriched()
