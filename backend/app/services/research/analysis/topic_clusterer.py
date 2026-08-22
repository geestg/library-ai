from __future__ import annotations

import re
from typing import List, Dict, Any
from collections import defaultdict


# Definisi Rumpun Tema Utama berdasarkan Kata Kunci Semantik
THEME_TAXONOMY = {
    "info_retrieval_clustering": {
        "cluster_name": "Temu Kembali Informasi, Klasifikasi & Clustering Dokumen",
        "keywords": [
            "clustering", "mdc", "k-means", "hierarchical", "tf-idf", "search",
            "pencarian", "temu kembali", "dspace", "perpustakaan", "dokumen",
            "klasifikasi teks", "nlp", "information retrieval", "arsip", "katalog"
        ]
    },
    "predictive_analytics_academic": {
        "cluster_name": "Pemodelan Prediktif & Analitik Perilaku/Performa Akademik",
        "keywords": [
            "prediksi", "kelulusan", "dropout", "mahasiswa", "akademik", "kepuasan",
            "perilaku", "evaluasi", "svm", "naive bayes", "random forest", "xgboost",
            "lightgbm", "decision tree", "klasifikasi data", "nilai", "prestasi"
        ]
    },
    "software_architecture_integration": {
        "cluster_name": "Rekayasa Perangkat Lunak, Arsitektur Sistem & Integrasi",
        "keywords": [
            "soa", "service oriented", "microservices", "api", "rest", "web",
            "sistem informasi", "arsitektur", "integrasi", "database", "basis data",
            "framework", "sdlc", "agile", "scrum", "manajemen tugas", "traceability"
        ]
    },
    "deep_learning_computer_vision": {
        "cluster_name": "Deep Learning, Computer Vision & Pemrosesan Sinyal",
        "keywords": [
            "cnn", "convolutional", "yolo", "resnet", "mobilenet", "citra",
            "vision", "deteksi objek", "segmentasi", "transformer", "bert",
            "vlm", "audio", "suara", "speech", "sar", "fpga"
        ]
    },
    "iot_embedded_edge": {
        "cluster_name": "Internet of Things, Sensor Fisik & Sistem Tertanam",
        "keywords": [
            "iot", "sensor", "arduino", "esp32", "raspberry", "cuaca",
            "monitoring", "suhu", "kelembapan", "embedded", "mikrokontroler",
            "lora", "real-time", "edge"
        ]
    },
    "bioprocess_kinetics_waste": {
        "cluster_name": "Kinetika Reaksi Bioproses, Bioreaktor & Pengolahan Limbah",
        "keywords": [
            "bioreaktor", "abr", "mbbr", "cstr", "mbr", "limbah", "fermentasi",
            "mikroba", "kinetika", "monod", "haldane", "luedeking", "cod", "bod",
            "tss", "biomassa", "biogas", "bioetanol"
        ]
    },
    "business_intelligence_governance": {
        "cluster_name": "Business Intelligence, Tata Kelola TI & Audit Sistem",
        "keywords": [
            "cobit", "itil", "togaf", "iso", "tata kelola", "governance",
            "dashboard", "business intelligence", "data warehouse", "bi",
            "audit", "compliance", "kpi", "scorecard", "analytics",
            "perencanaan strategis", "enterprise architecture", "maturity",
            "risk", "risiko", "kontrol internal", "indikator", "reporting"
        ]
    },
    "enterprise_adoption_process_mining": {
        "cluster_name": "Evaluasi Adopsi SI, Process Mining & Manajemen Proses Bisnis",
        "keywords": [
            "tam", "utaut", "delone", "mclean", "kepuasan pengguna", "penerimaan",
            "bpmn", "process mining", "erp", "crm", "enterprise", "reengineering",
            "proses bisnis", "evaluasi sistem", "system success", "adoption",
            "usability", "ueq", "sus", "service quality", "servqual",
            "decision support", "dss", "ahp", "topsis", "fuzzy", "spk"
        ]
    },
    "supply_chain_optimization": {
        "cluster_name": "Optimasi Rantai Pasok, Logistik & Manajemen Operasional",
        "keywords": [
            "rantai pasok", "supply chain", "logistik", "inventori", "gudang",
            "distribusi", "optimasi", "linear programming", "integer programming",
            "mip", "lean", "six sigma", "kopi", "karet", "kelayakan"
        ]
    },
    "networking_security_infrastructure": {
        "cluster_name": "Jaringan Komputer, Keamanan Jaringan & Infrastruktur TI (D3 TI)",
        "keywords": [
            "jaringan", "network", "router", "switch", "firewall", "vpn",
            "keamanan jaringan", "penetration testing", "wireshark", "cisco",
            "ospf", "vlan", "bandwidth", "monitoring jaringan", "packet",
            "protokol", "tcp", "ip", "dns", "dhcp", "proxy", "ids", "ips",
            "vulnerabilitas", "port scanning", "intrusion", "lan", "wan",
            "mikrotik", "qos", "throughput", "latency", "topologi"
        ]
    },
    "embedded_hardware_prototyping": {
        "cluster_name": "Embedded Systems, Prototyping Hardware & Otomasi (D3 TK)",
        "keywords": [
            "arduino", "esp32", "esp8266", "raspberry pi", "mikrokontroler",
            "embedded", "firmware", "prototipe", "sensor", "aktuator",
            "otomasi", "plc", "kontrol otomatis", "pwm", "adc", "uart",
            "i2c", "spi", "relay", "servo", "stepper", "motor dc",
            "instrumen", "pengukuran", "kalibrasi", "monitoring real-time",
            "sistem tertanam", "fpga", "vhdl", "verilog"
        ]
    }
}


def cluster_theses_by_topic(
    theses: List[Dict[str, Any]],
    query: str = "",
    min_cluster_size: int = 1,
    max_clusters: int = 5
) -> List[Dict[str, Any]]:
    """
    Mengelompokkan daftar skripsi repositori IT Del ke dalam klaster-klaster tematik
    untuk mendukung sintesis multi-dokumen (Multi-Document Gap Synthesis).

    Setiap paper hanya masuk ke SATU klaster berdasarkan kecocokan keyword terbaik.
    Paper unassigned didistribusikan round-robin ke klaster yang ada (bukan ditumpuk ke klaster[0]).
    """
    if not theses:
        return []

    # Map paper ke tema berdasarkan kecocokan kata kunci terbanyak
    cluster_buckets = defaultdict(list)
    unassigned = []

    for idx, t in enumerate(theses, start=1):
        title = (t.get("title") or t.get("judul") or "").lower()
        abstract = (t.get("abstract") or t.get("chunk") or "").lower()
        tech = " ".join(t.get("technologies", [])).lower()
        method = " ".join(t.get("methodologies", [])).lower()
        text_corpus = f"{title} {abstract} {tech} {method}"

        # Scoring: hitung match count per tema, ambil tema dengan skor tertinggi
        # Jika ada seri (tie), pilih tema pertama dalam definisi THEME_TAXONOMY
        best_theme_key = None
        best_match_count = 0

        for theme_key, theme_data in THEME_TAXONOMY.items():
            match_count = sum(1 for kw in theme_data["keywords"] if kw in text_corpus)
            if match_count > best_match_count:
                best_match_count = match_count
                best_theme_key = theme_key

        thesis_entry = {
            "citation_id": idx,
            "title": t.get("title") or "Skripsi IT Del",
            "author": t.get("author") or "Alumni IT Del",
            "year": t.get("year") or "-",
            "prodi": t.get("prodi") or "-",
            "abstract": (t.get("abstract") or t.get("chunk") or "")[:300],
            "technologies": t.get("technologies", []),
            "methodologies": t.get("methodologies", []),
            "raw": t
        }

        # Threshold 2: butuh minimal 2 keyword match agar masuk klaster
        # (threshold 1 terlalu longgar — paper apapun bisa masuk tema umum)
        if best_theme_key and best_match_count >= 2:
            cluster_buckets[best_theme_key].append(thesis_entry)
        elif best_theme_key and best_match_count == 1:
            # Match lemah: tandai sebagai unassigned, akan didistribusikan round-robin
            unassigned.append((best_theme_key, thesis_entry))
        else:
            unassigned.append((None, thesis_entry))

    # Format hasil klaster dari paper dengan match kuat (≥ 2 keyword)
    clusters = []
    for theme_key, items in cluster_buckets.items():
        if len(items) >= min_cluster_size:
            theme_meta = THEME_TAXONOMY.get(theme_key, {})
            clusters.append({
                "cluster_key": theme_key,
                "cluster_name": theme_meta.get("cluster_name", theme_key.replace("_", " ").title()),
                "theses_count": len(items),
                "theses": items,
                "citation_ids": [item["citation_id"] for item in items]
            })

    # Distribusi paper unassigned: round-robin merata ke klaster yang ada
    # Prioritaskan ke tema yang paling cocok (jika ada), fallback ke round-robin
    if unassigned and clusters:
        cluster_key_to_idx = {cl["cluster_key"]: i for i, cl in enumerate(clusters)}
        rr_pointer = 0
        for (preferred_theme, thesis_entry) in unassigned:
            # Coba masukkan ke klaster tema yang paling cocok (jika klaster itu ada)
            if preferred_theme and preferred_theme in cluster_key_to_idx:
                target_idx = cluster_key_to_idx[preferred_theme]
            else:
                # Round-robin ke klaster berikutnya
                target_idx = rr_pointer % len(clusters)
                rr_pointer += 1
            clusters[target_idx]["theses"].append(thesis_entry)
            clusters[target_idx]["citation_ids"].append(thesis_entry["citation_id"])
            clusters[target_idx]["theses_count"] += 1
    elif unassigned and not clusters:
        # Tidak ada klaster sama sekali — buat klaster umum dari semua paper
        all_items = [entry for (_, entry) in unassigned]
        clusters.append({
            "cluster_key": "general_research_cluster",
            "cluster_name": "Kajian Empiris Repositori Akademik IT Del",
            "theses_count": len(all_items),
            "theses": all_items,
            "citation_ids": [item["citation_id"] for item in all_items]
        })

    # Urutkan klaster berdasarkan jumlah paper terbanyak (prioritas sintesis)
    clusters.sort(key=lambda x: x["theses_count"], reverse=True)
    return clusters[:max_clusters]

