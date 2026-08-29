#!/usr/bin/env python3
"""
scripts/migrate_to_3nf.py
==========================
Script migrasi PostgreSQL untuk menormalisasi data sirkulasi dan log pengunjung
menjadi skema 3NF (tabel: anggota, buku, kunjungan, sirkulasi).

Jalankan di server/lokal setelah pull:
    python scripts/migrate_to_3nf.py
"""

import os
import sys
import glob
import re
import datetime
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

def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST, dbname=POSTGRES_DB,
        user=POSTGRES_USER, password=POSTGRES_PASS, port=POSTGRES_PORT
    )

def setup_schema(conn):
    """Membuat tabel-tabel 3NF dengan CASCADE drop untuk membersihkan struktur lama."""
    sql = """
    DROP TABLE IF EXISTS public.sirkulasi CASCADE;
    DROP TABLE IF EXISTS public.visitors CASCADE;
    DROP TABLE IF EXISTS public.kunjungan CASCADE;
    DROP TABLE IF EXISTS public.buku CASCADE;
    DROP TABLE IF EXISTS public.anggota CASCADE;

    CREATE TABLE public.anggota (
        ni TEXT PRIMARY KEY,
        nama TEXT NOT NULL,
        jabatan_jurusan TEXT
    );

    CREATE TABLE public.buku (
        id_master INTEGER PRIMARY KEY,
        judul TEXT NOT NULL
    );

    CREATE TABLE public.kunjungan (
        id SERIAL PRIMARY KEY,
        ni TEXT REFERENCES public.anggota(ni) ON DELETE CASCADE,
        visit_timestamp TIMESTAMP WITHOUT TIME ZONE,
        slot_waktu TEXT
    );

    CREATE TABLE public.sirkulasi (
        id VARCHAR(30) PRIMARY KEY,
        id_transaksi INTEGER,
        ni TEXT REFERENCES public.anggota(ni) ON DELETE CASCADE,
        id_master INTEGER REFERENCES public.buku(id_master) ON DELETE CASCADE,
        tanggal_pinjam DATE,
        batas_pengembalian DATE,
        tgl_kembali TIMESTAMP WITHOUT TIME ZONE,
        status VARCHAR(100),
        denda INTEGER DEFAULT 0
    );

    CREATE INDEX idx_kunjungan_ni ON public.kunjungan(ni);
    CREATE INDEX idx_kunjungan_ts ON public.kunjungan(visit_timestamp);
    CREATE INDEX idx_sirkulasi_ni ON public.sirkulasi(ni);
    CREATE INDEX idx_sirkulasi_id_master ON public.sirkulasi(id_master);
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("[DB] Skema 3NF berhasil dibuat.")

def find_file(pattern):
    _here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(_here, "..", "delbot_platform", "workflows", "dataset", pattern),
        os.path.join(_here, "..", "workflows", "dataset", pattern),
        f"/workspace/library-ai/delbot_platform/workflows/dataset/{pattern}",
    ]
    for c in candidates:
        found = glob.glob(c)
        if found:
            return found[0]
    return None

def main():
    vis_file = find_file("log_pengunjung_Genap_2026.xlsx")
    sir_file = find_file("Sirkulasi_Buku_Jan-Jul_2026.xlsx")

    if not vis_file or not sir_file:
        print("[ERROR] File Excel dataset tidak lengkap di server/lokal.")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"  MIGRASI 3NF DATABASE PERPUSTAKAAN")
    print(f"  Visitor Excel   : {vis_file}")
    print(f"  Sirkulasi Excel : {sir_file}")
    print(f"=======================================================\n")

    conn = get_connection()
    setup_schema(conn)

    # 1. Baca data Excel
    print("[MIGRATE] Membaca log pengunjung Excel...")
    df_vis = pd.read_excel(vis_file)
    df_vis.columns = [str(c).strip() for c in df_vis.columns]

    print("[MIGRATE] Membaca sirkulasi buku Excel...")
    df_sir = pd.read_excel(sir_file)
    df_sir.columns = [str(c).strip() for c in df_sir.columns]

    # 2. Proses Tabel Anggota (Merge unik dari Visitor & Sirkulasi)
    print("[MIGRATE] Memproses data anggota...")
    anggota_dict = {}

    # Masukkan dari sirkulasi first
    for _, row in df_sir.iterrows():
        ni = str(row.get("NI", "")).strip()
        nama = str(row.get("Nama", "")).strip()
        dept = str(row.get("Jabatan_Jurusan", "")).strip()
        if ni and ni.lower() != "nan" and ni not in anggota_dict:
            anggota_dict[ni] = (nama, dept)

    # Masukkan dari visitors (update/lengkapi jika belum ada)
    for _, row in df_vis.iterrows():
        ni = str(row.get("Nomor Anggota", "")).strip()
        nama = str(row.get("Nama", "")).strip()
        prodi = str(row.get("Prodi", "")).strip()
        if ni and ni.lower() != "nan":
            anggota_dict[ni] = (nama, prodi)

    anggota_rows = [(ni, val[0], val[1]) for ni, val in anggota_dict.items()]

    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO public.anggota (ni, nama, jabatan_jurusan) VALUES %s
        """, anggota_rows)
    conn.commit()
    print(f"[DB] {len(anggota_rows):,} baris anggota berhasil disimpan.")

    # 3. Proses Tabel Buku (Unik dari Sirkulasi)
    print("[MIGRATE] Memproses data buku...")
    buku_dict = {}
    for _, row in df_sir.iterrows():
        try:
            id_master = int(row.get("ID_Master_Buku"))
        except:
            continue
        judul = str(row.get("Judul", "Unknown")).strip()
        if id_master not in buku_dict:
            buku_dict[id_master] = judul

    buku_rows = [(k, v) for k, v in buku_dict.items()]
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO public.buku (id_master, judul) VALUES %s
        """, buku_rows)
    conn.commit()
    print(f"[DB] {len(buku_rows):,} baris buku berhasil disimpan.")

    # 4. Proses Tabel Kunjungan
    print("[MIGRATE] Memproses data log kunjungan...")
    kunjungan_rows = []
    tgl_col = [c for c in df_vis.columns if "tanggal" in c.lower() or "waktu" in c.lower()][0]

    for _, row in df_vis.iterrows():
        ni = str(row.get("Nomor Anggota", "")).strip()
        if ni not in anggota_dict:
            # Cegah constraint violation jika ada anggota tak terdaftar
            with conn.cursor() as cur:
                cur.execute("INSERT INTO public.anggota (ni, nama, jabatan_jurusan) VALUES (%s, %s, %s) ON CONFLICT (ni) DO NOTHING;", (ni, "Anggota Tanpa Nama", "Umum"))
            anggota_dict[ni] = ("Anggota Tanpa Nama", "Umum")

        raw_tgl = str(row.get(tgl_col, "")).strip()
        # Parse timestamp: e.g. "2026-01-06 09:02:05 (Slot: 08:00 - 11:59)"
        ts_match = re.match(r"^([\d\-:\s]+)", raw_tgl)
        slot_match = re.search(r"Slot:\s*([\d: -]+)", raw_tgl)

        ts = pd.to_datetime(ts_match.group(1).strip(), errors="coerce") if ts_match else None
        ts = ts.to_pydatetime() if not pd.isna(ts) else None
        slot = slot_match.group(1).strip() if slot_match else "Lainnya"

        kunjungan_rows.append((ni, ts, slot))

    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO public.kunjungan (ni, visit_timestamp, slot_waktu) VALUES %s
        """, kunjungan_rows)
    conn.commit()
    print(f"[DB] {len(kunjungan_rows):,} baris kunjungan berhasil disimpan.")

    # 5. Proses Tabel Sirkulasi
    print("[MIGRATE] Memproses data sirkulasi...")
    sirkulasi_rows = []
    today = datetime.date(2026, 7, 13)

    for idx, row in df_sir.iterrows():
        id_transaksi = int(row.get("ID_Transaksi", 0))
        ni = str(row.get("NI", "")).strip()
        if ni not in anggota_dict:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO public.anggota (ni, nama, jabatan_jurusan) VALUES (%s, %s, %s) ON CONFLICT (ni) DO NOTHING;", (ni, "Anggota Tanpa Nama", "Umum"))
            anggota_dict[ni] = ("Anggota Tanpa Nama", "Umum")

        try:
            id_master = int(row.get("ID_Master_Buku"))
        except:
            continue
        if id_master not in buku_dict:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO public.buku (id_master, judul) VALUES (%s, %s) ON CONFLICT (id_master) DO NOTHING;", (id_master, "Buku Tanpa Judul"))
            buku_dict[id_master] = "Buku Tanpa Judul"

        tgl_tx = row.get("Tgl_Transaksi")
        tgl_pinjam_val = pd.to_datetime(tgl_tx).date() if pd.notna(tgl_tx) else today

        rencana = row.get("Rencana_Kembali")
        rencana_dt = pd.to_datetime(rencana).date() if pd.notna(rencana) else today

        status = str(row.get("Kondisi_Pinjam", "Masih Dipinjam")).strip()
        tgl_kembali = row.get("Tgl_Kembali")
        tgl_kembali_ts = pd.to_datetime(tgl_kembali) if pd.notna(tgl_kembali) else None
        tgl_kembali_ts = tgl_kembali_ts.to_pydatetime() if tgl_kembali_ts else None

        denda_val = 0
        if pd.notna(tgl_kembali):
            kembali_dt = pd.to_datetime(tgl_kembali).date()
            if kembali_dt > rencana_dt:
                denda_val = (kembali_dt - rencana_dt).days * 2000
        else:
            if status == "Masih Dipinjam":
                if today > rencana_dt:
                    denda_val = (today - rencana_dt).days * 2000

        unique_id = f"TX_{idx:05d}"
        sirkulasi_rows.append((
            unique_id, id_transaksi, ni, id_master,
            tgl_pinjam_val, rencana_dt, tgl_kembali_ts, status, denda_val
        ))

    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO public.sirkulasi (id, id_transaksi, ni, id_master, tanggal_pinjam, batas_pengembalian, tgl_kembali, status, denda)
            VALUES %s
        """, sirkulasi_rows)
    conn.commit()
    print(f"[DB] {len(sirkulasi_rows):,} baris sirkulasi berhasil disimpan.")

    conn.close()
    print("\n✅ Migrasi database 3NF sukses sempurna!")

if __name__ == "__main__":
    main()
