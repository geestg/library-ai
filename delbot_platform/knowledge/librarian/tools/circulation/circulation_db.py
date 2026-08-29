from __future__ import annotations

import os
import psycopg2
import pandas as pd


class CirculationDBRepository:
    """
    Repository murni untuk mengelola koneksi database PostgreSQL,
    seeding data sirkulasi nyata, dan eksekusi kueri DataFrame.
    """

    def __init__(self):
        self._init_db()

    def get_db_connection(self):
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            database=os.getenv("POSTGRES_DB", "libraryai"),
            user=os.getenv("POSTGRES_USER", "libraryai"),
            password=os.getenv("POSTGRES_PASSWORD", "libraryai123"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )

    def _init_db(self):
        """
        Database initialization is now fully managed by scripts/migrate_to_3nf.py.
        This function just verifies if the schema is ready.
        """
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM public.anggota;")
            count = cur.fetchone()[0]
            print(f"[DB INIT] Database 3NF aktif dengan {count} anggota terdaftar.")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[DB INIT WARNING] Database 3NF belum dimigrasi atau tidak terhubung: {e}. Silakan jalankan 'python scripts/migrate_to_3nf.py'.")

    def get_loans_df(self) -> pd.DataFrame:
        """
        Mengambil data peminjaman buku murni dari database PostgreSQL 3NF dengan JOIN.
        """
        try:
            conn = self.get_db_connection()
            query = """
                SELECT 
                    s.id AS "ID Peminjaman",
                    s.id_transaksi AS "ID Transaksi",
                    a.nama AS "Nama Peminjam",
                    b.judul AS "Judul Buku",
                    s.tanggal_pinjam AS "Tanggal Pinjam",
                    s.batas_pengembalian AS "Batas Pengembalian",
                    s.status AS "Status",
                    s.denda AS "Denda (Rupiah)"
                FROM public.sirkulasi s
                JOIN public.anggota a ON s.ni = a.ni
                JOIN public.buku b ON s.id_master = b.id_master
                ORDER BY s.id ASC;
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            if not df.empty:
                df["Tanggal Pinjam"] = df["Tanggal Pinjam"].apply(lambda x: str(x))
                df["Batas Pengembalian"] = df["Batas Pengembalian"].apply(lambda x: str(x))
                return df
        except Exception as e:
            print(f"[CIRCULATION DB] Postgres connection failed ({e}), using direct Excel dataset fallback.")

        # Fallback langsung membaca dataset sirkulasi riil (3.620 transaksi)
        file_candidates = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx")),
            "/app/app/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx",
            "delbot_platform/workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx"
        ]
        excel_path = next((f for f in file_candidates if os.path.exists(f)), None)
        if excel_path:
            df_excel = pd.read_excel(excel_path)
            df_excel["ID Peminjaman"] = [f"TX_{i:05d}" for i in range(len(df_excel))]
            df_excel.rename(columns={
                "ID_Transaksi": "ID Transaksi",
                "Nama": "Nama Peminjam",
                "Judul": "Judul Buku",
                "Tgl_Transaksi": "Tanggal Pinjam",
                "Rencana_Kembali": "Batas Pengembalian",
                "Kondisi_Pinjam": "Status"
            }, inplace=True)
            if "Denda (Rupiah)" not in df_excel.columns:
                df_excel["Denda (Rupiah)"] = 0
            df_excel["Tanggal Pinjam"] = df_excel["Tanggal Pinjam"].apply(lambda x: str(x)[:10] if pd.notna(x) else "-")
            df_excel["Batas Pengembalian"] = df_excel["Batas Pengembalian"].apply(lambda x: str(x)[:10] if pd.notna(x) else "-")
            return df_excel

        return pd.DataFrame()
