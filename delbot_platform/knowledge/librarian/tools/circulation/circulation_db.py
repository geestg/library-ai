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
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            
            table_exists = False
            reseed_needed = False
            try:
                cur.execute("SELECT COUNT(*) FROM sirkulasi;")
                row_count = cur.fetchone()[0]
                table_exists = True
                
                cur.execute("SELECT denda FROM sirkulasi WHERE id = 'TX_00006';")
                val_row = cur.fetchone()
                if val_row and val_row[0] == 86000:
                    reseed_needed = True
            except Exception:
                row_count = 0
                conn.rollback()
            
            if not table_exists or row_count < 100 or reseed_needed:
                print("[DB INIT] Membuat ulang tabel sirkulasi dengan skema baru dari Excel...")
                cur.execute("DROP TABLE IF EXISTS sirkulasi;")
                cur.execute("""
                    CREATE TABLE sirkulasi (
                        id VARCHAR(30) PRIMARY KEY,
                        id_transaksi INT,
                        nama_peminjam VARCHAR(150),
                        judul_buku TEXT,
                        tanggal_pinjam DATE,
                        batas_pengembalian DATE,
                        status VARCHAR(100),
                        denda INT
                    );
                """)
                conn.commit()
                
                file_candidates = [
                    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx")),
                    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx")),
                    "/app/app/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx",
                    "delbot_platform/workflows/dataset/Sirkulasi_Buku_Jan-Jul_2026.xlsx"
                ]
                file_path = next((f for f in file_candidates if os.path.exists(f)), None)
                if file_path and os.path.exists(file_path):
                    print(f"[DB INIT] Membaca data dari {file_path}...")
                    df_excel = pd.read_excel(file_path)
                    
                    import datetime
                    today = datetime.date(2026, 7, 13)
                    
                    insert_data = []
                    for idx, row in df_excel.iterrows():
                        id_transaksi = int(row.get("ID_Transaksi", 0))
                        nama = str(row.get("Nama", "Unknown")).strip()
                        judul = str(row.get("Judul", "Unknown")).strip()
                        
                        tgl_tx = row.get("Tgl_Transaksi")
                        tgl_pinjam_val = pd.to_datetime(tgl_tx).date() if pd.notna(tgl_tx) else today
                        
                        rencana = row.get("Rencana_Kembali")
                        rencana_dt = pd.to_datetime(rencana).date() if pd.notna(rencana) else today
                        
                        status = str(row.get("Kondisi_Pinjam", "Masih Dipinjam")).strip()
                        tgl_kembali = row.get("Tgl_Kembali")
                        
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
                        
                        insert_data.append((
                            unique_id,
                            id_transaksi,
                            nama,
                            judul,
                            tgl_pinjam_val,
                            rencana_dt,
                            status,
                            denda_val
                        ))
                    
                    print(f"[DB INIT] Menyisipkan {len(insert_data)} baris data sirkulasi ke PostgreSQL...")
                    cur.executemany("""
                        INSERT INTO sirkulasi (id, id_transaksi, nama_peminjam, judul_buku, tanggal_pinjam, batas_pengembalian, status, denda)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, insert_data)
                    conn.commit()
                    print("[DB INIT] Seeding data sirkulasi berhasil!")
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[DB INIT ERROR] {e}")

    def get_loans_df(self) -> pd.DataFrame:
        """
        Mengambil 3.620 data peminjaman buku murni dari database PostgreSQL (atau fallback ke Excel).
        """
        try:
            conn = self.get_db_connection()
            query = "SELECT id AS \"ID Peminjaman\", id_transaksi AS \"ID Transaksi\", nama_peminjam AS \"Nama Peminjam\", judul_buku AS \"Judul Buku\", tanggal_pinjam AS \"Tanggal Pinjam\", batas_pengembalian AS \"Batas Pengembalian\", status AS \"Status\", denda AS \"Denda (Rupiah)\" FROM sirkulasi ORDER BY id ASC;"
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
