from __future__ import annotations

import os
import re
import pandas as pd
import psycopg2

UPLOAD_DIR = "/tmp/uploads"
REPORTS_DIR = "/tmp/uploads/reports"
DATASETS_DIR = "/app/app/dataset"

def _pg_connect():
    """Buka koneksi ke PostgreSQL dari env vars."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "libraryai"),
        user=os.getenv("POSTGRES_USER", "libraryai"),
        password=os.getenv("POSTGRES_PASSWORD", "libraryai123"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
    )

def _find_dataset_file(filename: str) -> str | None:
    _here = os.path.dirname(os.path.abspath(__file__))
    dirs = [
        os.path.join(_here, "../../../../workflows/dataset"),
        os.path.join(_here, "../../../../../workflows/dataset"),
        "/workspace/library-ai/delbot_platform/workflows/dataset",
        DATASETS_DIR, UPLOAD_DIR,
    ]
    for d in dirs:
        p = os.path.join(os.path.abspath(d), filename)
        if os.path.exists(p):
            return p
    return None

class VisitorSearchTool:
    """
    Tool khusus untuk mencari riwayat kunjungan anggota perpustakaan secara individu.
    Sumber utama: PostgreSQL 3NF. Fallback: Excel.
    """

    def search_visitor(self, member_query: str, filename: str = "log_pengunjung_Genap_2026.xlsx") -> str:
        """
        Mencari riwayat kunjungan anggota perpustakaan (berdasarkan nama atau NIM/Nomor Anggota)
        dan mengembalikan data statistik kunjungannya.
        """
        df: pd.DataFrame | None = None
        source_label = "PostgreSQL"
        tgl_col = "Tanggal Kunjungan"

        try:
            # Query matching member from DB
            query_clean = str(member_query).strip().lower()
            with _pg_connect() as conn:
                sql = """
                    SELECT a.ni               AS "Nomor Anggota",
                           a.nama             AS "Nama",
                           a.jabatan_jurusan  AS "Prodi",
                           k.visit_timestamp  AS "Tanggal Kunjungan",
                           k.slot_waktu       AS "Slot Waktu"
                    FROM public.kunjungan k
                    JOIN public.anggota   a ON k.ni = a.ni
                    WHERE LOWER(a.ni) LIKE %(q)s 
                       OR LOWER(a.nama) LIKE %(q)s
                    ORDER BY k.visit_timestamp ASC
                """
                df = pd.read_sql(sql, conn, params={"q": f"%{query_clean}%"})
            print(f"[VISITOR SEARCH] DB matched rows: {len(df)}")
        except Exception as db_err:
            print(f"[VISITOR SEARCH] DB error ({db_err}), fallback to Excel...")
            source_label = "Excel"
            file_path = _find_dataset_file(filename) or _find_dataset_file("log_pengunjung_Genap_2026.xlsx")
            if not file_path:
                return f"[TOOL_ERROR] Database tidak tersedia dan file log pengunjung `{filename}` tidak ditemukan."
            
            df_raw = pd.read_excel(file_path)
            df_raw.columns = [str(c).strip() for c in df_raw.columns]
            
            # Cari baris yang mencocokkan query secara fleksibel
            query_clean = str(member_query).strip().lower()
            query_words = [w for w in re.split(r'\W+', query_clean) if w]
            
            def is_match(row):
                name_str = str(row.get('Nama', '')).lower()
                nim_str = str(row.get('Nomor Anggota', '')).lower()
                if query_clean in nim_str:
                    return True
                if query_clean in name_str:
                    return True
                if query_words and all(word in name_str for word in query_words):
                    return True
                return False

            df = df_raw[df_raw.apply(is_match, axis=1)].copy()
            df.rename(columns={
                "Nomor Anggota": "Nomor Anggota",
                "Nama": "Nama",
                "Prodi": "Prodi",
            }, inplace=True)
            tgl_col = next((c for c in df.columns if 'tanggal' in c.lower() or 'waktu' in c.lower()), "Tanggal")

        if df is None or df.empty:
            return f"Tidak ditemukan data kunjungan untuk kata kunci pencarian: `{member_query}`."
            
        total_kunjungan = len(df)
        
        # Ambil detail anggota dari baris pertama yang cocok
        first_match = df.iloc[0]
        nama = first_match.get('Nama', member_query)
        nim = first_match.get('Nomor Anggota', 'N/A')
        prodi = first_match.get('Prodi', 'N/A')
        
        # List 5 kunjungan terakhir
        visits_list = ""
        recent_visits = df.tail(5)
        recent_list = []
        for idx, row in recent_visits.iterrows():
            t_val = row.get(tgl_col)
            slot_val = row.get("Slot Waktu")
            slot_str = f" (Slot: {slot_val})" if slot_val and pd.notna(slot_val) else ""
            recent_list.append(f"- Kunjungan pada: `{str(t_val)[:19]}{slot_str}`")
        recent_list.reverse()
        visits_list = "\n".join(recent_list)
            
        # Hitung jam terfavorit berkunjung
        slot_info = "N/A"
        if total_kunjungan > 0:
            if "Slot Waktu" in df.columns:
                slot_counts = df["Slot Waktu"].value_counts()
                if not slot_counts.empty:
                    fav_slot = slot_counts.index[0]
                    fav_slot_count = slot_counts.iloc[0]
                    slot_info = f"**{fav_slot}** ({fav_slot_count} kali berkunjung pada slot ini)"
            else:
                def extract_slot(t):
                    m = re.search(r'Slot:\s*([\d:]+\s*-\s*[\d:]+)', str(t))
                    return m.group(1) if m else 'Lainnya'
                df['Slot'] = df[tgl_col].apply(extract_slot)
                slot_counts = df['Slot'].value_counts()
                if not slot_counts.empty:
                    fav_slot = slot_counts.index[0]
                    fav_slot_count = slot_counts.iloc[0]
                    slot_info = f"**{fav_slot}** ({fav_slot_count} kali berkunjung pada slot ini)"

        report = (
            f"### 🔍 Hasil Pencarian Riwayat Pengunjung Perpustakaan ({source_label}):\n\n"
            f"👤 **Profil Anggota:**\n"
            f"- **Nama:** {nama}\n"
            f"- **NIM/Nomor Anggota:** `{nim}`\n"
            f"- **Program Studi:** {prodi}\n\n"
            f"📊 **Statistik Kunjungan:**\n"
            f"- Total Kunjungan: **{total_kunjungan} kali**\n"
            f"- Slot Waktu Terfavorit: {slot_info}\n\n"
            f"📅 **5 Kunjungan Terakhir:**\n{visits_list}"
        )
        return report

