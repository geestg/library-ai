from __future__ import annotations

import os
import re
import pandas as pd

UPLOAD_DIR = "/tmp/uploads"
REPORTS_DIR = "/tmp/uploads/reports"
DATASETS_DIR = "/app/app/dataset"


class VisitorSearchTool:
    """
    Tool khusus untuk mencari riwayat kunjungan anggota perpustakaan secara individu.
    """

    def search_visitor(self, member_query: str, filename: str = "log_pengunjung_Genap_2026.xlsx") -> str:
        """
        Mencari riwayat kunjungan anggota perpustakaan (berdasarkan nama atau NIM/Nomor Anggota)
        dan mengembalikan data statistik kunjungannya.
        """
        paths_to_check = [
            os.path.join(DATASETS_DIR, filename),
            os.path.join(UPLOAD_DIR, filename),
            os.path.join("/app/app/dataset", filename)
        ]
        
        file_path = next((p for p in paths_to_check if os.path.exists(p)), None)
        if not file_path:
            return "Berkas log pengunjung tidak ditemukan untuk melakukan pencarian."

        try:
            df = pd.read_excel(file_path)
            df.columns = [str(c).strip() for c in df.columns]
            
            # Cari baris yang mencocokkan query secara fleksibel
            query_clean = str(member_query).strip().lower()
            query_words = [w for w in re.split(r'\W+', query_clean) if w]
            
            def is_match(row):
                name_str = str(row.get('Nama', '')).lower()
                nim_str = str(row.get('Nomor Anggota', '')).lower()
                if query_clean in nim_str:
                    return True
                # Jika query_clean adalah substring langsung, cocokkan
                if query_clean in name_str:
                    return True
                # Jika berupa kata pencarian, pastikan semua kata pencarian ada di nama target
                if query_words and all(word in name_str for word in query_words):
                    return True
                return False

            matched_df = df[df.apply(is_match, axis=1)].copy()
            
            if matched_df.empty:
                return f"Tidak ditemukan data kunjungan untuk kata kunci pencarian: `{member_query}`."
                
            total_kunjungan = len(matched_df)
            
            # Ambil detail anggota dari baris pertama yang cocok
            first_match = matched_df.iloc[0]
            nama = first_match['Nama']
            nim = first_match['Nomor Anggota']
            prodi = first_match['Prodi']
            
            # List 5 kunjungan terakhir
            tgl_col = next((c for c in matched_df.columns if 'tanggal' in c.lower() or 'waktu' in c.lower()), None)
            visits_list = ""
            if tgl_col:
                recent_visits = matched_df.tail(5)
                recent_list = []
                for idx, row in recent_visits.iterrows():
                    recent_list.append(f"- Kunjungan pada: `{row[tgl_col]}`")
                recent_list.reverse()
                visits_list = "\n".join(recent_list)
                
            # Hitung jam terfavorit berkunjung
            slot_info = "N/A"
            if tgl_col and total_kunjungan > 0:
                def extract_slot(t):
                    m = re.search(r'Slot:\s*([\d:]+\s*-\s*[\d:]+)', str(t))
                    return m.group(1) if m else 'Lainnya'
                matched_df['Slot'] = matched_df[tgl_col].apply(extract_slot)
                slot_counts = matched_df['Slot'].value_counts()
                if not slot_counts.empty:
                    fav_slot = slot_counts.index[0]
                    fav_slot_count = slot_counts.iloc[0]
                    slot_info = f"**{fav_slot}** ({fav_slot_count} kali berkunjung pada slot ini)"

            report = (
                f"### 🔍 Hasil Pencarian Riwayat Pengunjung Perpustakaan:\n\n"
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
            
        except Exception as e:
            return f"Gagal mencari riwayat pengunjung: {str(e)}"
