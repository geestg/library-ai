from __future__ import annotations

import hashlib
import uuid
from typing import Any, Dict, List
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from qdrant_client.models import PointStruct

from app.core.constants import LIBRARY_BOOKS_COLLECTION
from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client, ensure_collection_exists
from app.services.library.data.book_preparation import BookPreparation
from app.services.library.data.book_transformer import BookTransformer

EXCEL_PATH = "/app/app/dataset/dapus.xlsx"
BATCH_SIZE = 100  # Proses per 100 buku untuk menghemat RAM
MAX_WORKERS = 10  # 10 thread paralel


class BookIngest:
    """
    Pipeline bertahap (incremental) dan resumable untuk ingest data katalog buku dari Excel ke Qdrant.
    """
    def __init__(self, excel_path: str = EXCEL_PATH):
        self.preparation = BookPreparation(excel_path)
        self.transformer = BookTransformer()

    def build_point_id(self, item: Dict[str, Any]) -> str:
        # Gunakan field termutasi (sanitized) khusus untuk hashing
        title = item.get("_hash_title") or str(item.get("title") or "").strip().lower()
        author = item.get("_hash_author") or str(item.get("author") or "").strip().lower()
        isbn = str(item.get("isbn") or "").strip().lower()
        
        # Jika ISBN kosong, bertanda -/none, atau merupakan placeholder dummy, gunakan judul + penulis
        if not isbn or isbn == "-" or isbn.lower() == "none" or isbn.startswith("979000") or isbn.startswith("978000") or len(isbn) < 5:
            unique_key = f"{title}_{author}"
        else:
            unique_key = f"{title}_{author}_{isbn}"
            
        hashed = hashlib.md5(unique_key.encode("utf-8")).hexdigest()
        return str(uuid.UUID(hashed))

    def get_existing_ids(self) -> set[str]:
        """
        Mengambil semua ID point yang sudah terdaftar di Qdrant agar bisa skip data lama.
        """
        print("[CHECK] Memeriksa data lama di Qdrant...")
        existing_ids = set()
        try:
            limit = 10000
            offset = None
            while True:
                response = client.scroll(
                    collection_name=LIBRARY_BOOKS_COLLECTION,
                    limit=limit,
                    with_payload=False,
                    with_vectors=False,
                    offset=offset
                )
                points, next_offset = response
                for p in points:
                    existing_ids.add(p.id)
                if not next_offset:
                    break
                offset = next_offset
            print(f"[CHECK] Ditemukan {len(existing_ids)} buku sudah ter-index sebelumnya.")
        except Exception as e:
            print(f"[CHECK WARNING] Gagal cek data lama (mungkin koleksi baru): {e}")
        return existing_ids

    def process_single_book(self, raw_book: Dict[str, Any], idx: int) -> PointStruct | None:
        if not self.preparation.validate_book(raw_book):
            return None
            
        try:
            transformed = self.transformer.transform_book(raw_book)
            text_to_embed = transformed.get("text", "")
            
            if not text_to_embed.strip():
                return None

            point_id = self.build_point_id(transformed)
            
            # Request embedding ke Ollama
            embedding = get_embedding(text_to_embed)
            return PointStruct(
                id=point_id,
                vector=embedding,
                payload=transformed
            )

        except Exception as e:
            title = raw_book.get("Title") or raw_book.get("judul") or "Unknown"
            print(f"[INGEST ERROR] #{idx+1} '{title[:30]}': {e}")
            return None

    def ingest(self):
        print("\n" + "=" * 60)
        print("STARTING INCREMENTAL & RESUMABLE BOOK INGESTION")
        print("=" * 60)

        # 1. Pastikan koleksi siap (768 dim)
        ensure_collection_exists(LIBRARY_BOOKS_COLLECTION, vector_size=768)

        # 2. Ambil data ID yang sudah masuk untuk resumable
        existing_ids = self.get_existing_ids()

        # 3. Load excel
        try:
            raw_books = self.preparation.load_books()
        except Exception as e:
            print(f"[INGEST ERROR] Gagal load Excel: {e}")
            sys.exit(1)

        total_books = len(raw_books)
        points_batch = []
        skipped = 0
        success_count = 0
        failed_count = 0

        # Filter buku yang belum di-index dan hilangkan duplikasi dalam berkas Excel
        todo_books = []
        seen_todo_ids = set()
        for idx, book in enumerate(raw_books):
            if not self.preparation.validate_book(book):
                continue
            transformed = self.transformer.transform_book(book)
            point_id = self.build_point_id(transformed)
            
            if point_id in existing_ids:
                skipped += 1
            elif point_id in seen_todo_ids:
                skipped += 1
            else:
                seen_todo_ids.add(point_id)
                todo_books.append((idx, book))

        print(f"[RESUME] Total: {total_books} | Skipped (Sudah ada): {skipped} | Sisa proses: {len(todo_books)}")

        if not todo_books:
            print("[DONE] Semua buku sudah ter-index dengan lengkap!")
            return

        # 4. Proses per batch (misal 100 buku)
        for i in range(0, len(todo_books), BATCH_SIZE):
            chunk = todo_books[i : i + BATCH_SIZE]
            points_batch = []
            
            # Jalankan embedding paralel khusus untuk batch ini
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(self.process_single_book, book, idx): idx 
                    for idx, book in chunk
                }
                for future in as_completed(futures):
                    try:
                        point = future.result()
                        if point:
                            points_batch.append(point)
                            success_count += 1
                        else:
                            failed_count += 1
                    except Exception:
                        failed_count += 1

            # Langsung upload ke Qdrant begitu batch ini selesai
            if points_batch:
                client.upsert(
                    collection_name=LIBRARY_BOOKS_COLLECTION,
                    points=points_batch
                )
                
            processed_so_far = skipped + success_count + failed_count
            print(f"[PROGRESS] {processed_so_far}/{total_books} terproses (Success batch ini: {len(points_batch)}, Total Success: {success_count}, Failed: {failed_count})")
            
            # Kosongkan list untuk bebaskan memori RAM
            points_batch.clear()

        print(f"\n[DONE] Ingest selesai! Berhasil menambahkan {success_count} buku baru. (Total failed: {failed_count})")
        print("=" * 60)

if __name__ == "__main__":
    ingester = BookIngest()
    ingester.ingest()
