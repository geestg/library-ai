#!/usr/bin/env python3
"""
scripts/import_visitor_to_db.py
================================
Script sekali-jalan untuk mengimpor data log pengunjung dari file Excel
ke tabel `visitors` di PostgreSQL (database: libraryai).

Jalankan SEKALI di server setelah git pull:
    cd /workspace/library-ai
    python scripts/import_visitor_to_db.py

Dengan --clear untuk menghapus data lama sebelum import:
    python scripts/import_visitor_to_db.py --clear
"""

import os, sys, glob, argparse
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

_here = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_here, "..", ".env"))

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB   = os.getenv("POSTGRES_DB",   "libraryai")
POSTGRES_USER = os.getenv("POSTGRES_USER", "libraryai")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "libraryai123")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

# Mapping kolom Excel (lowercase) -> kolom DB
COLUMN_MAP = {
    "nomor anggota": "member_id", "no anggota": "member_id",
    "nim": "member_id", "id": "member_id", "member_id": "member_id",
    "nama": "name", "name": "name",
    "prodi": "study_program", "program studi": "study_program",
    "study_program": "study_program", "jurusan": "study_program",
    "tanggal": "visit_timestamp", "waktu": "visit_timestamp",
    "waktu kunjungan": "visit_timestamp", "tanggal kunjungan": "visit_timestamp",
    "visit_timestamp": "visit_timestamp", "timestamp": "visit_timestamp",
    "status": "status", "keterangan": "status",
    "kategori": "category_role", "role": "category_role",
    "category_role": "category_role", "peran": "category_role",
    "jenis anggota": "category_role",
}

def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST, dbname=POSTGRES_DB,
        user=POSTGRES_USER, password=POSTGRES_PASS, port=POSTGRES_PORT
    )

def ensure_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS public.visitors (
        member_id     TEXT,
        name          TEXT,
        study_program TEXT,
        visit_timestamp TIMESTAMP WITHOUT TIME ZONE,
        status        TEXT,
        category_role VARCHAR(100)
    );
    CREATE INDEX IF NOT EXISTS idx_visitors_study_program ON public.visitors (study_program);
    CREATE INDEX IF NOT EXISTS idx_visitors_category_role ON public.visitors (category_role);
    CREATE INDEX IF NOT EXISTS idx_visitors_ts ON public.visitors (visit_timestamp);
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("[DB] Tabel visitors sudah siap.")

def load_excel(filepath):
    print(f"[IMPORT] Membaca: {filepath}")
    df = pd.read_excel(filepath)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def map_columns(df):
    rename = {col: COLUMN_MAP[col] for col in df.columns if col in COLUMN_MAP}
    df = df.rename(columns=rename)
    for col in ["member_id","name","study_program","visit_timestamp","status","category_role"]:
        if col not in df.columns:
            df[col] = None
    return df[["member_id","name","study_program","visit_timestamp","status","category_role"]]

def import_dataframe(conn, df, clear_first=False):
    rows = []
    for _, row in df.iterrows():
        ts = pd.to_datetime(row["visit_timestamp"], errors="coerce")
        ts = ts.to_pydatetime() if not pd.isna(ts) else None
        rows.append((
            str(row["member_id"]) if pd.notna(row["member_id"]) else None,
            str(row["name"]) if pd.notna(row["name"]) else None,
            str(row["study_program"]) if pd.notna(row["study_program"]) else None,
            ts,
            str(row["status"]) if pd.notna(row["status"]) else None,
            str(row["category_role"]) if pd.notna(row["category_role"]) else None,
        ))
    with conn.cursor() as cur:
        if clear_first:
            cur.execute("TRUNCATE TABLE public.visitors;")
            print("[DB] Data lama dihapus (--clear mode).")
        execute_values(cur, """
            INSERT INTO public.visitors
                (member_id, name, study_program, visit_timestamp, status, category_role)
            VALUES %s
        """, rows, page_size=500)
        print(f"[DB] {len(rows):,} baris berhasil dimasukkan.")
    conn.commit()

def find_excel_file():
    candidates = [
        "delbot_platform/workflows/dataset/log_pengunjung_Genap_2026.xlsx",
        "/workspace/library-ai/delbot_platform/workflows/dataset/log_pengunjung_Genap_2026.xlsx",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    found = glob.glob("delbot_platform/workflows/dataset/log_pengunjung*.xlsx")
    return found[0] if found else None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", default=None)
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    filepath = args.file or find_excel_file()
    if not filepath or not os.path.exists(filepath):
        print("[ERROR] File Excel tidak ditemukan. Gunakan: --file /path/ke/log_pengunjung.xlsx")
        sys.exit(1)

    print(f"\n{'='*55}")
    print(f"  IMPORT LOG PENGUNJUNG -> PostgreSQL")
    print(f"  File : {filepath}")
    print(f"  DB   : {POSTGRES_USER}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"{'='*55}\n")

    conn = get_connection()
    ensure_table(conn)
    df = map_columns(load_excel(filepath))
    print(f"[IMPORT] {len(df):,} baris terdeteksi")
    import_dataframe(conn, df, clear_first=args.clear)
    conn.close()
    print("\nImport selesai! Cek dengan: SELECT COUNT(*) FROM visitors;\n")

if __name__ == "__main__":
    main()
