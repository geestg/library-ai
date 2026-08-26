import os
import sys
import json
import uuid
import time
import re
from qdrant_client.models import PointStruct

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from delbot_platform.research.retrieval.embedder import get_embedding
from delbot_platform.research.retrieval.qdrant_client import client, ensure_collection_exists
from delbot_platform.core.constants import THESIS_DATASET_COLLECTION

DATASET_PATH = os.path.join(PROJECT_ROOT, "delbot_platform", "workflows", "dataset", "skripsi_dataset_enriched.json")
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
BATCH_SIZE = 32

PRODI_ALIASES = {
    "MI D3": "Informatika",
    "Manajemen Informatika": "Informatika",
}

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\r\n", " ", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
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

def build_chunks(item: dict) -> list:
    title = clean_text(item.get("title", ""))
    author = clean_text(item.get("author", ""))
    year = item.get("year", "")
    prodi = item.get("prodi", "")
    url = item.get("url", "")
    keywords = item.get("keywords", [])
    content = item.get("content") or {}

    prodi = PRODI_ALIASES.get(prodi, prodi)

    base_payload = {
        "title": title,
        "author": author,
        "year": year,
        "prodi": prodi,
        "url": url,
        "keywords": keywords,
    }

    all_chunks = []

    # 1. Abstract
    abstract = clean_text(content.get("abstract", ""))
    if not abstract:
        abstract = clean_text(item.get("abstract", ""))

    if abstract:
        text = f"Judul: {title}\nAbstrak: {abstract}"
        all_chunks.append({
            **base_payload,
            "source_bab": "abstract",
            "source_label": "Abstrak",
            "chunk_index": 0,
            "chunk": clean_text(text),
        })

    # 2. Bab 1, 3, 5
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
                "source_bab": bab_key,
                "source_label": bab_label,
                "chunk_index": idx,
                "chunk": sub,
            })

    return all_chunks

def run_ingestion():
    print("=" * 70, flush=True)
    print("      DELBOT QDRANT THESIS DATASET INGESTOR (EMBED & UPSERT)   ", flush=True)
    print("=" * 70, flush=True)
    print(f"Target Collection : {THESIS_DATASET_COLLECTION}", flush=True)
    print(f"Dataset Path      : {DATASET_PATH}", flush=True)

    if not os.path.exists(DATASET_PATH):
        print(f"[ERROR] Dataset file not found at {DATASET_PATH}", flush=True)
        return

    # Check embedding dimension (MiniLM 384, bge-m3 1024, nomic 768)
    sample_vec = get_embedding("Test embedding dimension")
    dim = len(sample_vec)
    print(f"[EMBEDDER] Active embedding vector dimension: {dim}", flush=True)

    # 1. Hapus koleksi lama dan buat baru (Fresh Re-Ingest)
    from qdrant_client.models import Distance, VectorParams
    try:
        collections = client.get_collections()
        exists = any(c.name == THESIS_DATASET_COLLECTION for c in collections.collections)
        if exists:
            client.delete_collection(collection_name=THESIS_DATASET_COLLECTION)
            print(f"[QDRANT] Koleksi lama '{THESIS_DATASET_COLLECTION}' BERHASIL DIHAPUS (Reset Clean).", flush=True)
        client.create_collection(
            collection_name=THESIS_DATASET_COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )
        print(f"[QDRANT] Koleksi baru '{THESIS_DATASET_COLLECTION}' BERHASIL DIBUAT (Dimensi: {dim}).", flush=True)
    except Exception as reset_err:
        print(f"[QDRANT RESET WARNING] {reset_err}. Menggunakan ensure_collection_exists.", flush=True)
        ensure_collection_exists(THESIS_DATASET_COLLECTION, vector_size=dim)

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"[LOAD] {len(dataset)} thesis records loaded from JSON", flush=True)

    all_chunk_dicts = []
    for item in dataset:
        all_chunk_dicts.extend(build_chunks(item))

    total_chunks = len(all_chunk_dicts)
    print(f"[CHUNKER] {total_chunks} total text chunks generated from dataset", flush=True)

    if total_chunks == 0:
        print("[ERROR] No chunks available to ingest.", flush=True)
        return

    points_buffer = []
    success = 0
    errors = 0
    start_time = time.time()

    for i, chunk_dict in enumerate(all_chunk_dicts, 1):
        chunk_text_val = chunk_dict.get("chunk", "")
        if not chunk_text_val:
            continue

        try:
            vector = get_embedding(chunk_text_val)
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk_dict,
            )
            points_buffer.append(point)
            success += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"[EMBED ERROR] Chunk {i}: {e}", flush=True)
            continue

        if len(points_buffer) >= BATCH_SIZE:
            try:
                client.upsert(
                    collection_name=THESIS_DATASET_COLLECTION,
                    points=points_buffer,
                )
                elapsed = time.time() - start_time
                rate = success / max(1, elapsed)
                pct = (i / total_chunks) * 100
                print(f"[{i}/{total_chunks}] ({pct:.1f}%) - Upserted: {success} chunks | {rate:.1f} chunks/s | Errors: {errors}", flush=True)
            except Exception as e:
                print(f"[QDRANT UPSERT ERROR] {e}", flush=True)
            points_buffer = []

    # Final flush
    if points_buffer:
        try:
            client.upsert(
                collection_name=THESIS_DATASET_COLLECTION,
                points=points_buffer,
            )
        except Exception as e:
            print(f"[QDRANT FLUSH ERROR] {e}", flush=True)

    elapsed = time.time() - start_time
    print("=" * 70, flush=True)
    print(f"INGESTION COMPLETE in {elapsed:.1f} seconds!", flush=True)
    print(f"Total chunks successfully upserted to Qdrant: {success}", flush=True)
    print(f"Total errors: {errors}", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    run_ingestion()
