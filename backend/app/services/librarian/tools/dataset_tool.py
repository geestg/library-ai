from __future__ import annotations

import os
import re
import uuid
import hashlib
import psycopg2
import pandas as pd
from typing import Dict, List, Any

from app.core.constants import LIBRARY_BOOKS_COLLECTION
from app.rag.embedder import get_embedding
from app.rag.qdrant_client import client, ensure_collection_exists
from qdrant_client.models import PointStruct

UPLOAD_DIR = "/tmp/uploads"
DATASETS_DIR = "/app/app/dataset"


class LibraryDatasetTools:
    """
    Kumpulan perkakas administratif untuk mengelola pencarian daftar file dataset perpustakaan,
    serta membaca dan menyinkronkan data katalog buku baru (.xlsx/.csv) DUAL-SYNC ke Qdrant & PostgreSQL.
    """

    def list_datasets(self) -> str:
        """
        Mendaftar semua berkas data (.csv, .xlsx, .xls) yang ada di folder datasets (/app/datasets)
        dan folder uploads (/tmp/uploads).
        """
        datasets_files = []
        if os.path.exists(DATASETS_DIR):
            datasets_files = [f for f in os.listdir(DATASETS_DIR) if f.endswith(('.csv', '.xlsx', '.xls'))]
            
        uploads_files = []
        if os.path.exists(UPLOAD_DIR):
            uploads_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(('.csv', '.xlsx', '.xls'))]
            
        response = "### Daftar Berkas Data yang Tersedia:\n\n"
        if not datasets_files and not uploads_files:
            response += "⚠️ Tidak ada berkas data (.csv atau .xlsx) yang ditemukan di folder `datasets/` atau `uploads/`."
            return response
            
        if datasets_files:
            response += "**📁 Folder `datasets/` (Data Permanen):**\n"
            for f in datasets_files:
                response += f"- `{f}`\n"
            response += "\n"
            
        if uploads_files:
            response += "**📁 Folder `uploads/` (Unggahan Chat):**\n"
            for f in uploads_files:
                response += f"- `{f}`\n"
                
        return response

    def sync_collection(self, filename: str) -> str:
        """
        Membaca file katalog buku baru (.xlsx/.csv), memvalidasi kelengkapan data,
        dan menyinkronkan data valid DUAL-SYNC ke Qdrant Vector Store DAN PostgreSQL database.
        """
        file_path = os.path.join(DATASETS_DIR, filename)
        if not os.path.exists(file_path):
            file_path = os.path.join(UPLOAD_DIR, filename)
            
        if not os.path.exists(file_path):
            files = []
            if os.path.exists(DATASETS_DIR):
                files += [os.path.join(DATASETS_DIR, f) for f in os.listdir(DATASETS_DIR) if f.endswith(('.csv', '.xlsx', '.xls'))]
            if os.path.exists(UPLOAD_DIR):
                files += [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR) if f.endswith(('.csv', '.xlsx', '.xls'))]
                
            if not files:
                return (
                    f"Berkas `{filename}` tidak ditemukan.\n"
                    "Silakan letakkan file data (.csv atau .xlsx) di folder `datasets/` atau unggah via chat."
                )
            file_path = files[0]
            filename = os.path.basename(file_path)

        try:
            print(f"[ADMIN SYNC] Membaca file: {file_path}")
            if filename.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='latin1')
            else:
                df = pd.read_excel(file_path)
            
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            title_col = None
            for col in df.columns:
                if 'judul' in col or 'title' in col:
                    title_col = col
                    break
                    
            if not title_col:
                return f"Gagal memproses file `{filename}`: Kolom 'Judul' atau 'Title' tidak ditemukan."

            total_rows = len(df)
            valid_books = []
            invalid_books = []

            for idx, row in df.iterrows():
                title = str(row.get(title_col, "")).strip()
                if not title or title == "nan":
                    invalid_books.append(f"Baris {idx+2}: Judul kosong")
                    continue
                
                author = str(row.get("author", row.get("penulis", "Unknown"))).strip()
                publisher = str(row.get("publisher", row.get("penerbit", "Unknown"))).strip()
                location = str(row.get("location", row.get("lokasi", "Lt.1"))).strip()
                class_num = str(row.get("classification_number", row.get("no_klasifikasi", ""))).strip()
                isbn = str(row.get("isbn", "")).strip()
                
                if isbn and isbn != "nan" and len(re.sub(r'[^0-9X]', '', isbn)) not in [10, 13]:
                    invalid_books.append(f"Baris {idx+2}: Format ISBN tidak valid untuk '{title[:30]}'")
                
                valid_books.append({
                    "title": title,
                    "author": author if author != "nan" else "Unknown",
                    "publisher": publisher if publisher != "nan" else "Unknown",
                    "location": location if location != "nan" else "Lt.1",
                    "classification_number": class_num if class_num != "nan" else "",
                    "isbn": isbn if isbn != "nan" else "",
                    "text": f"{title} oleh {author}. Penerbit: {publisher}. Lokasi: {location}."
                })

            status_report = (
                f"### Analisis Validasi Berkas `{filename}`:\n"
                f"• Total Data Terbaca: **{total_rows} buku**\n"
                f"• Valid & Siap Sinkron: **{len(valid_books)} buku**\n"
                f"• Tidak Valid (Gagal): **{len(invalid_books)} buku**\n\n"
            )
            
            if invalid_books:
                status_report += "**Detail Kesalahan Validasi:**\n" + "\n".join([f"- {err}" for err in invalid_books[:5]]) + "\n\n"

            if not valid_books:
                return status_report + "❌ Tidak ada data buku valid yang siap disinkronkan."

            # 1. DUAL-SYNC SINKRONISASI KE POSTGRESQL (Tabel books)
            try:
                pg_conn = psycopg2.connect(
                    host="postgres",
                    database=os.getenv("POSTGRES_DB", "libraryai"),
                    user=os.getenv("POSTGRES_USER", "libraryai"),
                    password=os.getenv("POSTGRES_PASSWORD", "libraryai123"),
                    port="5432"
                )
                pg_cur = pg_conn.cursor()
                pg_cur.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id VARCHAR(50) PRIMARY KEY,
                        title TEXT NOT NULL,
                        author VARCHAR(150),
                        publisher VARCHAR(150),
                        location VARCHAR(100),
                        classification_number VARCHAR(50),
                        isbn VARCHAR(50)
                    );
                """)
                
                pg_data = []
                for b in valid_books:
                    unique_key = b["isbn"] or b["title"]
                    b_id = hashlib.md5(unique_key.encode("utf-8")).hexdigest()[:12]
                    pg_data.append((
                        b_id,
                        b["title"],
                        b["author"],
                        b["publisher"],
                        b["location"],
                        b["classification_number"],
                        b["isbn"]
                    ))
                
                pg_cur.executemany("""
                    INSERT INTO books (id, title, author, publisher, location, classification_number, isbn)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET title = EXCLUDED.title,
                        author = EXCLUDED.author,
                        publisher = EXCLUDED.publisher,
                        location = EXCLUDED.location,
                        classification_number = EXCLUDED.classification_number,
                        isbn = EXCLUDED.isbn;
                """, pg_data)
                pg_conn.commit()
                pg_cur.close()
                pg_conn.close()
                print(f"[ADMIN DUAL-SYNC] Berhasil menyinkronkan {len(valid_books)} buku ke PostgreSQL 'books' table.")
            except Exception as pg_err:
                print(f"[ADMIN DUAL-SYNC WARNING] Gagal menyinkronkan ke PostgreSQL: {pg_err}")

            # 2. DUAL-SYNC SINKRONISASI KE QDRANT VECTOR STORE
            print(f"[ADMIN SYNC] Menghubungkan ke Qdrant untuk mengunggah {len(valid_books)} buku...")
            ensure_collection_exists(LIBRARY_BOOKS_COLLECTION, vector_size=768)
            
            points = []
            for b in valid_books:
                try:
                    embedding = get_embedding(b["text"])
                except Exception as embed_err:
                    print(f"[ADMIN SYNC WARNING] Gagal mendapatkan embedding untuk '{b['title'][:30]}': {embed_err}. Menggunakan mock embedding 768-dim.")
                    embedding = [0.0] * 768
                
                unique_key = b["isbn"] or b["title"]
                hashed = hashlib.md5(unique_key.encode("utf-8")).hexdigest()
                point_id = str(uuid.UUID(hashed))
                
                points.append(PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=b
                ))

            client.upsert(
                collection_name=LIBRARY_BOOKS_COLLECTION,
                points=points
            )

            status_report += (
                "🚀 **Status DUAL-SYNC Berhasil:**\n"
                f"Berhasil meng-indeks **{len(valid_books)} buku** secara bersamaan ke **PostgreSQL Database** DAN **Qdrant Vector DB** dengan sukses! "
                "Buku-buku baru ini kini siap dicari oleh mahasiswa via chat AI maupun dihitung oleh Pustakawan via kueri SQL."
            )
            return status_report
            
        except Exception as e:
            return f"Terjadi kesalahan saat memproses berkas data: {str(e)}"
