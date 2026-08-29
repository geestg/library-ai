from __future__ import annotations

import os
import re
import uuid
import json
import glob
import pandas as pd

UPLOAD_DIR = "/tmp/uploads"
REPORTS_DIR = "/tmp/uploads/reports"
DATASETS_DIR = "/app/app/dataset"

def _find_dataset_file(filename: str) -> str | None:
    """
    Mencari file dataset secara dinamis di berbagai lokasi yang mungkin,
    baik di server Docker maupun lokal. Mengembalikan path absolute jika ditemukan.
    """
    # Path berbasis __file__ (relative dari visitor_analytics.py)
    _here = os.path.dirname(os.path.abspath(__file__))
    candidate_dirs = [
        os.path.join(_here, "../../../../workflows/dataset"),      # /delbot_platform/workflows/dataset
        os.path.join(_here, "../../../../../workflows/dataset"),   # satu level lebih atas
        os.path.join(_here, "../../../../dataset"),                # fallback dataset di delbot_platform
        "/workspace/library-ai/delbot_platform/workflows/dataset",# path absolut server GPU
        "/workspace/library-ai/delbot_platform/dataset",
        "/app/app/dataset",
        "/app/dataset",
        DATASETS_DIR,
        UPLOAD_DIR,
    ]
    
    # Cek exact match dulu
    for d in candidate_dirs:
        p = os.path.join(os.path.abspath(d), filename)
        if os.path.exists(p):
            return p
    
    # Glob fallback: cari di seluruh workspace
    patterns = [
        f"/workspace/**/{filename}",
        f"/app/**/{filename}",
    ]
    for pat in patterns:
        found = glob.glob(pat, recursive=True)
        if found:
            return found[0]
    
    # Cari berdasarkan keyword jika nama file tidak exact match
    keyword = "pengunjung"
    for d in candidate_dirs:
        d_abs = os.path.abspath(d)
        if os.path.exists(d_abs):
            for f in os.listdir(d_abs):
                if keyword in f.lower() and f.endswith((".xlsx", ".csv", ".xls")):
                    return os.path.join(d_abs, f)
    
    return None


class VisitorAnalyticsTool:
    """
    Tool khusus untuk mengurai data log pengunjung perpustakaan,
    menghitung statistik prodi, jam sibuk, dan dashboard Chart.js.
    """

    def analyze_visitor_log(self, filename: str = "log_pengunjung_Genap_2026.xlsx", month: str | int | None = None) -> str:
        """
        Tool khusus untuk mengurai data log pengunjung perpustakaan,
        menghitung statistik prodi, jam sibuk, dan daftar pengunjung teraktif.
        Dapat difilter berdasarkan bulan.
        """
        file_path = _find_dataset_file(filename)
        if not file_path:
            file_path = _find_dataset_file("log_pengunjung_Genap_2026.xlsx")
        if not file_path:
            return (
                f"[TOOL_ERROR] Berkas log pengunjung `{filename}` tidak ditemukan di seluruh direktori server. "
                "Pastikan file log_pengunjung_Genap_2026.xlsx ada di folder delbot_platform/workflows/dataset/."
            )
        filename = os.path.basename(file_path)


        try:
            print(f"[ADMIN ANALYTICS] Menganalisis berkas log pengunjung: {file_path}")
            df = pd.read_excel(file_path)
            
            df.columns = [str(c).strip() for c in df.columns]
            
            tgl_col = None
            for c in df.columns:
                if 'tanggal' in c.lower() or 'waktu' in c.lower():
                    tgl_col = c
                    break

            month_info_str = ""
            if month and tgl_col:
                month_str = str(month).strip().lower()
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
                    "desember": "12", "des": "12", "12": "12"
                }
                target_month = month_map.get(month_str)
                if target_month:
                    def get_month(x):
                        try:
                            part = str(x).split()[0].split('-')
                            return part[1] if len(part) > 1 else ''
                        except Exception:
                            return ''
                    df['Month_Part'] = df[tgl_col].apply(get_month)
                    df = df[df['Month_Part'] == target_month]
                    
                    month_names = {
                        "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
                        "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
                        "09": "September", "10": "Oktober", "11": "November", "12": "Desember"
                    }
                    month_info_str = f" Khusus Bulan **{month_names.get(target_month, month_str)}**"

            total_kunjungan = len(df)
            if total_kunjungan == 0:
                return f"Tidak ditemukan data log pengunjung untuk Bulan `{month}` di berkas `{filename}`."
            
            prodi_counts = df['Prodi'].value_counts().head(5).reset_index()
            prodi_counts.columns = ['Program Studi', 'Jumlah Kunjungan']
            prodi_table = prodi_counts.to_markdown(index=False)
            
            top_visitors = df.groupby(['Nomor Anggota', 'Nama', 'Prodi']).size().reset_index(name='Kunjungan')
            top_visitors = top_visitors.sort_values(by='Kunjungan', ascending=False).head(5)
            top_visitors.columns = ['Nomor Anggota', 'Nama', 'Program Studi', 'Jumlah Kunjungan']
            top_visitors_table = top_visitors.to_markdown(index=False)
            
            top_prodis = df['Prodi'].value_counts().head(2).index.tolist()
            prodi_1 = top_prodis[0] if len(top_prodis) > 0 else "N/A"
            prodi_2 = top_prodis[1] if len(top_prodis) > 1 else "N/A"

            ALL_STUDENT_PRODIS = [
                "S1 Informatika",
                "S1 Sistem Informasi",
                "D3 Teknologi Informasi",
                "D3 Teknologi Komputer",
                "S1 Teknik Elektro",
                "D4 Sarjana Terapan Teknologi Rekayasa Perangkat Lunak",
                "S1 Manajemen Rekayasa",
                "S1 Teknik BioProses",
                "S1 Bioteknologi",
                "S1 Teknik Metalurgi"
            ]
            visited_prodis = set(df['Prodi'].unique())
            zero_visit_prodis = [p for p in ALL_STUDENT_PRODIS if p not in visited_prodis]
            
            extra_rec_str = ""
            if zero_visit_prodis:
                prodis_zero = ", ".join(f"**{p}**" for p in zero_visit_prodis[:2])
                extra_rec_str = f"- **Jangkauan Prodi Pasif (0 Kunjungan)**: Program Studi {prodis_zero} tercatat memiliki 0 kunjungan pada periode ini. Disarankan melakukan sosialisasi terarah atau berkoordinasi dengan Kaprodi untuk mengevaluasi ketersediaan buku teks wajib mata kuliah mereka di perpustakaan."
            else:
                student_df = df[df['Prodi'].isin(ALL_STUDENT_PRODIS)]
                if not student_df.empty:
                    lowest_prodis = student_df['Prodi'].value_counts(ascending=True).head(2).index.tolist()
                    if len(lowest_prodis) > 0:
                        prodi_low1 = lowest_prodis[0]
                        prodi_low2 = lowest_prodis[1] if len(lowest_prodis) > 1 else lowest_prodis[0]
                        if prodi_low1 == prodi_low2:
                            extra_rec_str = f"- **Peningkatan Aktivitas Prodi Terendah**: Program Studi **{prodi_low1}** memiliki tingkat kunjungan terendah. Disarankan mengadakan mini-exhibition koleksi buku spesifik rumpun ilmu mereka di area lobi perpustakaan."
                        else:
                            extra_rec_str = f"- **Peningkatan Aktivitas Prodi Terendah**: Program Studi **{prodi_low1}** dan **{prodi_low2}** memiliki tingkat kunjungan terendah. Disarankan mengadakan program sosialisasi/library tour terarah untuk mendorong keterlibatan mahasiswa prodi tersebut."
                else:
                    extra_rec_str = "- **Sosialisasi Koleksi Umum**: Kunjungan mahasiswa non-IT sangat minim. Disarankan menyelenggarakan pameran buku fiksi atau umum untuk menarik minat baca lintas prodi."

            slot_table = ""
            avg_daily_str = "N/A"
            slot_1 = "08:00 - 11:59"
            slot_2 = "12:00 - 15:59"
            combined_percent = 90.0

            if tgl_col:
                def extract_slot(t):
                    m = re.search(r'Slot:\s*([\d:]+\s*-\s*[\d:]+)', str(t))
                    slot_val = m.group(1) if m else 'Lainnya'
                    # Map the raw early morning slot to actual library start hours (7 AM) to prevent confusion
                    if slot_val == '04:00 - 07:59':
                        return '07:00 - 07:59'
                    return slot_val
                df['Slot'] = df[tgl_col].apply(extract_slot)
                slot_counts = df['Slot'].value_counts().reset_index()
                slot_counts.columns = ['Slot Waktu', 'Jumlah Kunjungan']
                slot_table = slot_counts.to_markdown(index=False)
                
                top_slots_df = df['Slot'].value_counts().head(2)
                top_slots = top_slots_df.index.tolist()
                if len(top_slots) > 0:
                    slot_1 = top_slots[0]
                if len(top_slots) > 1:
                    slot_2 = top_slots[1]
                if total_kunjungan > 0:
                    combined_percent = (top_slots_df.sum() / total_kunjungan) * 100

                df['Tanggal_Only'] = df[tgl_col].apply(lambda x: str(x).split()[0])
                avg_daily = df['Tanggal_Only'].value_counts().mean()
                avg_daily_rounded = int(round(avg_daily)) if not pd.isna(avg_daily) else 0
                avg_daily_str = f"{avg_daily_rounded:,} pengunjung/hari"
                
            base_name = os.path.splitext(filename)[0]
            short_hash = uuid.uuid4().hex[:6]
            if month:
                month_clean_name = str(month).replace(" ", "_")
                export_filename = f"{base_name}_bulan_{month_clean_name}_{short_hash}.xlsx"
            else:
                export_filename = f"{base_name}_lengkap_{short_hash}.xlsx"
            
            export_path = os.path.join(REPORTS_DIR, export_filename)
            os.makedirs(REPORTS_DIR, exist_ok=True)
            
            cols_to_export = [c for c in df.columns if c not in ['Month_Part', 'Slot', 'Tanggal_Only']]
            df[cols_to_export].to_excel(export_path, index=False, sheet_name="Log Pengunjung")
            download_url = f"http://127.0.0.1:8000/reports/{export_filename}"

            # Prepare data for Markdown table
            bar_chart_str = "#### 🏫 Distribusi Kunjungan per Prodi\n[BAR_CHART]\n"

            report = (
                f"### 📊 Laporan Analisis Log Pengunjung Perpustakaan{month_info_str}\n\n"
                f"*Unduh data log pengunjung terfilter format Excel:* [{export_filename}]({download_url})\n\n"
                f"#### 📈 Ringkasan Kunjungan\n"
                f"- **Total Kunjungan:** {total_kunjungan:,} kunjungan\n"
                f"- **Rata-rata Harian:** {avg_daily_str}\n\n"
                f"{bar_chart_str}"
                f"#### 👥 Top 5 Pengunjung Terloyal\n{top_visitors_table}\n\n"
                f"#### ⏰ Distribusi Jam Kunjungan\n{slot_table}\n\n"
                "#### 💡 Rekomendasi Operasional\n"
                f"- **Penambahan Staf Gerbang Masuk**: Puncak kepadatan terjadi pada slot **{slot_1}** dan **{slot_2}** (menyumbang {combined_percent:.1f}% kunjungan). Disarankan menambah staf penjaga gerbang masuk pada jam-jam sibuk tersebut.\n"
                f"- **Promosi Koleksi IT Prioritas**: Program Studi **{prodi_1}** dan **{prodi_2}** menyumbang kunjungan terbesar. Promosi koleksi buku baru dapat diprioritaskan untuk kategori komputasi/IT.\n"
                f"{extra_rec_str}"
            )
            
            # Return dict with text and structured data for charting
            return {
                "text": report,
                "data": prodi_counts.to_dict(orient="records")
            }
            
        except Exception as e:
            return {
                "text": f"Gagal menganalisis log pengunjung: {str(e)}",
                "data": []
            }
