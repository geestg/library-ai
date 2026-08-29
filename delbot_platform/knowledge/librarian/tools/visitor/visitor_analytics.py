from __future__ import annotations

import os
import re
import uuid
import glob
import pandas as pd
import psycopg2

# ──────────────────────────────────────────────────────────────────────────────
UPLOAD_DIR   = "/tmp/uploads"
REPORTS_DIR  = "/tmp/uploads/reports"
DATASETS_DIR = "/app/app/dataset"

# ──────────────────────────────────────────────────────────────────────────────
def _pg_connect():
    """Buka koneksi ke PostgreSQL dari env vars."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "libraryai"),
        user=os.getenv("POSTGRES_USER", "libraryai"),
        password=os.getenv("POSTGRES_PASSWORD", "libraryai123"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
    )


def _load_visitors_from_db(month_num: str | None = None) -> pd.DataFrame:
    """Query tabel visitors dari PostgreSQL, opsional filter per bulan."""
    with _pg_connect() as conn:
        if month_num:
            sql = """
                SELECT member_id       AS "Nomor Anggota",
                       name            AS "Nama",
                       study_program   AS "Prodi",
                       visit_timestamp AS "Tanggal Kunjungan",
                       status,
                       category_role
                FROM public.visitors
                WHERE EXTRACT(MONTH FROM visit_timestamp) = %(m)s
                  AND visit_timestamp IS NOT NULL
                ORDER BY visit_timestamp
            """
            df = pd.read_sql(sql, conn, params={"m": int(month_num)})
        else:
            sql = """
                SELECT member_id       AS "Nomor Anggota",
                       name            AS "Nama",
                       study_program   AS "Prodi",
                       visit_timestamp AS "Tanggal Kunjungan",
                       status,
                       category_role
                FROM public.visitors
                ORDER BY visit_timestamp
            """
            df = pd.read_sql(sql, conn)
    return df


def _find_dataset_file(filename: str) -> str | None:
    """Fallback: cari file Excel di berbagai lokasi."""
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
    for pat in [f"/workspace/**/{filename}", f"/app/**/{filename}"]:
        found = glob.glob(pat, recursive=True)
        if found:
            return found[0]
    for d in dirs:
        d_abs = os.path.abspath(d)
        if os.path.exists(d_abs):
            for f in os.listdir(d_abs):
                if "pengunjung" in f.lower() and f.endswith((".xlsx", ".csv", ".xls")):
                    return os.path.join(d_abs, f)
    return None


class VisitorAnalyticsTool:
    """
    Analisis log pengunjung perpustakaan.
    Sumber data UTAMA : tabel `visitors` di PostgreSQL.
    Fallback           : file Excel di workflows/dataset/.
    """

    def analyze_visitor_log(
        self,
        filename: str = "log_pengunjung_Genap_2026.xlsx",
        month: str | int | None = None,
    ) -> str | dict:
        """
        Analisis log pengunjung, dapat difilter per bulan.
        Nama bulan bisa Indonesia ('maret') atau angka (3 / '03').
        """
        month_map = {
            "januari": "01", "jan": "01", "1": "01", "01": "01",
            "februari": "02", "feb": "02", "2": "02", "02": "02",
            "maret": "03", "mar": "03", "3": "03", "03": "03",
            "april": "04", "apr": "04", "4": "04", "04": "04",
            "mei": "05", "5": "05", "05": "05",
            "juni": "06", "jun": "06", "6": "06", "06": "06",
            "juli": "07", "jul": "07", "7": "07", "07": "07",
            "agustus": "08", "ags": "08", "8": "08", "08": "08",
            "september": "09", "sep": "09", "9": "09", "09": "09",
            "oktober": "10", "okt": "10", "10": "10",
            "november": "11", "nov": "11", "11": "11",
            "desember": "12", "des": "12", "12": "12",
        }
        month_names = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
            "05": "Mei",     "06": "Juni",     "07": "Juli",  "08": "Agustus",
            "09": "September", "10": "Oktober", "11": "November", "12": "Desember",
        }

        target_month: str | None = None
        month_info_str = ""
        if month is not None:
            target_month = month_map.get(str(month).strip().lower())
            if target_month:
                month_info_str = f" Khusus Bulan **{month_names.get(target_month, str(month))}**"

        # ── Muat data ────────────────────────────────────────────────────
        df: pd.DataFrame | None = None
        source_label = "PostgreSQL"
        tgl_col = "Tanggal Kunjungan"

        try:
            df = _load_visitors_from_db(month_num=target_month)
            print(f"[VISITOR ANALYTICS] DB: {len(df):,} baris")
        except Exception as db_err:
            print(f"[VISITOR ANALYTICS] DB gagal ({db_err}), coba Excel...")
            source_label = "Excel"
            fp = _find_dataset_file(filename) or _find_dataset_file("log_pengunjung_Genap_2026.xlsx")
            if not fp:
                return (
                    "[TOOL_ERROR] PostgreSQL tidak tersedia DAN file Excel tidak ditemukan. "
                    "Jalankan: python scripts/import_visitor_to_db.py"
                )
            df = pd.read_excel(fp)
            df.columns = [str(c).strip() for c in df.columns]
            tgl_col = next(
                (c for c in df.columns if "tanggal" in c.lower() or "waktu" in c.lower()), None
            )
            if target_month and tgl_col:
                df["_m"] = df[tgl_col].apply(
                    lambda x: (str(x).split()[0].split("-")[1] if "-" in str(x) else "")
                )
                df = df[df["_m"] == target_month]

        if df is None or len(df) == 0:
            return (
                f"Tidak ada data pengunjung"
                f"{f' bulan {str(month)}' if month else ''}. "
                "Import data dulu: python scripts/import_visitor_to_db.py"
            )

        total_kunjungan = len(df)
        prodi_col = next(
            (c for c in ["Prodi", "study_program"] if c in df.columns), df.columns[2]
        )
        id_col   = "Nomor Anggota" if "Nomor Anggota" in df.columns else "member_id"
        nama_col = "Nama"          if "Nama"          in df.columns else "name"

        # Statistik prodi
        prodi_counts = df[prodi_col].value_counts().head(5).reset_index()
        prodi_counts.columns = ["Program Studi", "Jumlah Kunjungan"]
        prodi_table = prodi_counts.to_markdown(index=False)

        # Top pengunjung
        top_vis = (
            df.groupby([id_col, nama_col, prodi_col]).size()
            .reset_index(name="Kunjungan")
            .sort_values("Kunjungan", ascending=False).head(5)
        )
        top_vis.columns = ["Nomor Anggota", "Nama", "Program Studi", "Jumlah Kunjungan"]
        top_visitors_table = top_vis.to_markdown(index=False)

        prodi_list = prodi_counts["Program Studi"].tolist()
        prodi_1 = prodi_list[0] if prodi_list else "N/A"
        prodi_2 = prodi_list[1] if len(prodi_list) > 1 else "N/A"

        # Prodi dengan nol kunjungan
        ALL_PRODIS = [
            "S1 Informatika", "S1 Sistem Informasi", "D3 Teknologi Informasi",
            "D3 Teknologi Komputer", "S1 Teknik Elektro",
            "D4 Sarjana Terapan Teknologi Rekayasa Perangkat Lunak",
            "S1 Manajemen Rekayasa", "S1 Teknik BioProses",
            "S1 Bioteknologi", "S1 Teknik Metalurgi",
        ]
        visited = set(df[prodi_col].unique())
        zero_p  = [p for p in ALL_PRODIS if p not in visited]
        if zero_p:
            pz = ", ".join(f"**{p}**" for p in zero_p[:2])
            extra_rec = f"- **Prodi Pasif (0 Kunjungan)**: {pz}. Disarankan sosialisasi terarah."
        else:
            st_df = df[df[prodi_col].isin(ALL_PRODIS)]
            if not st_df.empty:
                lowest = st_df[prodi_col].value_counts(ascending=True).head(2).index.tolist()
                pl = lowest[0]
                pl2 = lowest[1] if len(lowest) > 1 else pl
                extra_rec = f"- **Prodi Terendah**: **{pl}** & **{pl2}**. Library tour disarankan."
            else:
                extra_rec = "- **Sosialisasi Umum**: Kunjungan masih minim lintas prodi."

        # Distribusi jam
        slot_table, avg_daily_str = "", "N/A"
        slot_1, slot_2, combined_percent = "08:00-11:59", "12:00-15:59", 90.0
        tgl_actual = tgl_col if tgl_col and tgl_col in df.columns else None

        if tgl_actual:
            def extract_slot(t):
                try:
                    ts = pd.to_datetime(t, errors="coerce")
                    if pd.isna(ts): return "Lainnya"
                    h = ts.hour
                    if 4  <= h < 8:  return "04:00-07:59"
                    if 8  <= h < 12: return "08:00-11:59"
                    if 12 <= h < 16: return "12:00-15:59"
                    if 16 <= h < 20: return "16:00-19:59"
                    return "Lainnya"
                except Exception:
                    return "Lainnya"

            df["Slot"] = df[tgl_actual].apply(extract_slot)
            sc = df["Slot"].value_counts().reset_index()
            sc.columns = ["Slot Waktu", "Jumlah Kunjungan"]
            slot_table = sc.to_markdown(index=False)
            top_s = df["Slot"].value_counts().head(2)
            tsl   = top_s.index.tolist()
            slot_1 = tsl[0] if tsl else slot_1
            slot_2 = tsl[1] if len(tsl) > 1 else slot_2
            combined_percent = (top_s.sum() / total_kunjungan * 100) if total_kunjungan else 90.0

            df["_d"] = df[tgl_actual].apply(
                lambda x: str(pd.to_datetime(x, errors="coerce").date()) if pd.notna(x) else "N/A"
            )
            avg = df["_d"].value_counts().mean()
            avg_daily_str = f"{int(round(avg)):,} pengunjung/hari" if not pd.isna(avg) else "N/A"

        # Export Excel laporan
        short_h    = uuid.uuid4().hex[:6]
        base_name  = os.path.splitext(filename)[0]
        export_fn  = (
            f"{base_name}_bulan_{str(month).replace(' ','_')}_{short_h}.xlsx"
            if month else f"{base_name}_lengkap_{short_h}.xlsx"
        )
        export_path = os.path.join(REPORTS_DIR, export_fn)
        os.makedirs(REPORTS_DIR, exist_ok=True)
        cols_x = [c for c in df.columns if c not in ["_m", "_d", "Slot"]]
        df[cols_x].to_excel(export_path, index=False, sheet_name="Log Pengunjung")
        dl_url = f"http://127.0.0.1:8000/reports/{export_fn}"

        report = (
            f"### Laporan Analisis Log Pengunjung Perpustakaan{month_info_str}\n"
            f"*Sumber: {source_label}* | "
            f"[Unduh Excel]({dl_url})\n\n"
            f"#### Ringkasan Kunjungan\n"
            f"- **Total:** {total_kunjungan:,} kunjungan\n"
            f"- **Rata-rata Harian:** {avg_daily_str}\n\n"
            f"#### Top 5 Program Studi\n{prodi_table}\n\n"
            f"#### Top 5 Pengunjung Terloyal\n{top_visitors_table}\n\n"
            f"#### Distribusi Jam Kunjungan\n{slot_table}\n\n"
            f"#### Rekomendasi Operasional\n"
            f"- **Staf Gerbang**: Puncak di **{slot_1}** & **{slot_2}** "
            f"({combined_percent:.1f}% kunjungan).\n"
            f"- **Promosi Koleksi**: Prodi **{prodi_1}** & **{prodi_2}** paling aktif.\n"
            f"{extra_rec}\n"
        )

        return {"text": report, "data": prodi_counts.to_dict(orient="records")}
