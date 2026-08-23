import json
import re
from typing import Optional, Dict, Any

class InterviewState:
    """
    State Machine Container untuk Wawancara Skripsi Mahasiswa.
    Menyimpan informasi prodi, jenjang, fakultas, dan topik yang terdeteksi.
    """
    def __init__(self):
        self.prodi: Optional[str] = None
        self.jenjang: Optional[str] = None
        self.fakultas: Optional[str] = None
        self.topic: Optional[str] = None
        self.has_menu_been_presented: bool = False


class InterviewPlanner:
    """
    Agent State Machine Planner untuk DELBot Berbasis Knowledge Base Institusional IT Del.
    Mendukung pengelompokan Fakultas (FITE, FTI, Vokasi) & Jenjang (D3, D4, S1).
    """

    # =====================================================
    # KNOWLEDGE BASE PROGRAM STUDI INSTITUSIONAL IT DEL
    # =====================================================
    PROGRAM_STUDI = {
        # FAKULTAS INFORMATIKA & TEKNIK ELEKTRO (FITE)
        "Sistem Informasi": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "si", "sistem informasi", "sisfo", "prodi si", "jurusan si",
                "sistem informasi s1", "sif", "sistem info", "s1 si",
                "sistem informasi s-1"
            ]
        },
        "Informatika": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "if", "informatika", "prodi if", "jurusan if",
                "ilmu komputer", "informaika", "informatika s1",
                "infromatika", "informtika", "informatica",
                "s1 informatika", "s1 if", "teknik informatika"
            ]
        },
        "Teknologi Informasi": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "ti", "teknologi informasi", "prodi ti", "jurusan ti",
                "teknologi informasi s1", "ti s1", "s1 ti",
                "teknik informasi", "teknologi informatika"
            ]
        },
        "Teknik Elektro": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "te", "elektro", "teknik elektro", "elktro",
                "elektro s1", "teknik eletro", "teknik elekro",
                "s1 elektro", "s1 te", "electrical engineering"
            ]
        },
        "Teknik Bioproses": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "tb", "bioproses", "teknik bioproses", "bioprosess",
                "teknik bioprosess", "bio proses", "teknik bio proses",
                "bioprocess", "bioproses s1", "bio proses s1",
                "s1 bioproses", "s1 tb"
            ]
        },
        "Bioteknologi": {
            "jenjang": "S1",
            "fakultas": "FITE",
            "aliases": [
                "biotek", "bioteknologi", "bio teknologi", "biotechnology",
                "bioteknology", "s1 bioteknologi", "s1 biotek"
            ]
        },

        # FAKULTAS TEKNIK INDUSTRI (FTI)
        "Manajemen Rekayasa": {
            "jenjang": "S1",
            "fakultas": "FTI",
            "aliases": [
                "mr", "manajemen rekayasa", "rekayasa manajemen",
                "manajemen rekayasa s1", "mr s1", "s1 mr",
                "management engineering", "manajemen rekayasa industri"
            ]
        },
        "Teknik Metalurgi": {
            "jenjang": "S1",
            "fakultas": "FTI",
            "aliases": [
                "tm", "metalurgi", "teknik metalurgi", "metalurg",
                "metalurgi s1", "s1 metalurgi", "s1 tm",
                "metallurgy", "metalurgy"
            ]
        },

        # FAKULTAS VOKASI
        "D4 Teknologi Rekayasa Perangkat Lunak": {
            "jenjang": "D4",
            "fakultas": "Vokasi",
            "aliases": [
                "trpl", "d4 trpl", "teknologi rekayasa perangkat lunak",
                "rekayasa perangkat lunak", "rpl", "d4 rpl",
                "d4 rekayasa perangkat lunak", "rekayasa software",
                "software engineering vokasi"
            ]
        },
        "D3 Teknologi Komputer": {
            "jenjang": "D3",
            "fakultas": "Vokasi",
            "aliases": [
                "tk", "d3 tk", "teknologi komputer",
                "d3 teknologi komputer", "komputer d3",
                "d3 komputer", "teknologi komputer d3"
            ]
        },
        "D3 Teknologi Informasi": {
            "jenjang": "D3",
            "fakultas": "Vokasi",
            "aliases": [
                "d3 ti", "d3 teknologi informasi",
                "teknologi informasi d3", "ti d3",
                "d3 teknik informasi", "d3ti"
            ]
        }
    }

    # PRODI_MAP dibentuk secara otomatis dari Knowledge Base
    PRODI_MAP = {
        alias.lower(): prodi_name
        for prodi_name, info in PROGRAM_STUDI.items()
        for alias in info["aliases"]
    }

    TOPIC_MAP = {
        "1": "AI & Smart Systems",
        "2": "Data Analytics & BI",
        "3": "Enterprise Web/Mobile",
        "4": "Health/Edu Tech",
        "5": "Tren Populer IT Del",
        "ai": "AI & Smart Systems",
        "artificial intelligence": "AI & Smart Systems",
        "data": "Data Analytics & BI",
        "analytics": "Data Analytics & BI",
        "bi": "Data Analytics & BI",
        "web": "Enterprise Web/Mobile",
        "mobile": "Enterprise Web/Mobile",
        "health": "Health/Edu Tech",
        "edu": "Health/Edu Tech",
        "iot": "IoT & Embedded Systems",
        "nlp": "NLP & Language AI",
        "smart": "AI & Smart Systems",
        "tren": "Tren Populer IT Del",
        "supply chain": "Supply Chain & Logistics",
        "manufacturing": "Smart Manufacturing & Industry 4.0",
        "metalurgi": "AI & Metallurgy Analytics",
        "software": "Applied Software Development",
        "software engineering": "Applied Software Development",
        "rekayasa perangkat lunak": "Applied Software Development",
        "microservices": "Applied Software Development",
        "applied software": "Applied Software Development",
        "backend": "Applied Software Development",
        "frontend": "Applied Software Development",
        "devops": "Applied Software Development",
        "architecture": "Applied Software Development",
        "cloud": "Applied Software Development",
        "ci/cd": "Applied Software Development",
        "database": "Data Analytics & BI",
        "basis data": "Data Analytics & BI",
        "machine learning": "AI & Smart Systems",
        "deep learning": "AI & Smart Systems",
        "recommendation": "AI & Smart Systems",
        "rekomendasi": "AI & Smart Systems",
        "rag": "AI & Smart Systems",
        "embedded systems": "IoT & Embedded Systems",
        "embedded systems & iot": "IoT & Embedded Systems",
        "iot & embedded systems": "IoT & Embedded Systems",
        "embedded": "IoT & Embedded Systems",
        "kontrol": "Sistem Kontrol & Otomasi Industri",
        "otomasi": "Sistem Kontrol & Otomasi Industri",
        "power systems": "Power Systems & Renewable Energy",
        "renewable": "Power Systems & Renewable Energy",
        "signal processing": "Signal Processing & Robotics",
        "robotics": "Signal Processing & Robotics",
        "tren populer": "Tren Populer IT Del",
    }

    PRODI_SELECTION_TOPICS = {
        "Teknik Bioproses": {
            "1": "Bioprocess Simulation & Fermentation Control",
            "2": "Bioreactor Modeling & Kinetics",
            "3": "Biomass & Bioresource Analytics",
            "4": "Enzyme & Downstream Processing",
            "5": "Tren Populer IT Del",
        },
        "Bioteknologi": {
            "1": "Bioinformatics & Molecular Data Mining",
            "2": "Genomic Sequence Analytics",
            "3": "Industrial Biotechnology",
            "4": "Medical & Agricultural Biotech",
            "5": "Tren Populer IT Del",
        },
        "Teknik Elektro": {
            "1": "Sistem Kontrol & Otomasi Industri",
            "2": "Power Systems & Renewable Energy",
            "3": "Signal Processing & Robotics",
            "4": "Embedded Systems & IoT",
            "5": "Tren Populer IT Del",
        },
        "Teknik Metalurgi": {
            "1": "Mineral Processing & Flotation Analytics",
            "2": "Pyrometallurgy & Hydrometallurgy Modeling",
            "3": "Corrosion Analytics & Material Degradation",
            "4": "Extractive Metallurgy",
            "5": "Tren Populer IT Del",
        },
        "Manajemen Rekayasa": {
            "1": "Supply Chain Management & Logistics",
            "2": "Quality Control & Six Sigma (DMAIC)",
            "3": "Industrial Process Optimization",
            "4": "Operations Research & Inventory Systems",
            "5": "Tren Populer IT Del",
        },
        "Sistem Informasi": {
            "1": "Business Process Re-engineering & BPMN",
            "2": "Enterprise Systems (ERP Odoo/CRM)",
            "3": "Business Intelligence & BI Dashboards",
            "4": "IT Governance & Audit (ITIL/COBIT)",
            "5": "AI & Smart Information Systems",
        },
        "Informatika": {
            "1": "Advanced AI & Deep Learning",
            "2": "Natural Language Processing & RAG",
            "3": "Computer Vision & Image Analytics",
            "4": "Distributed Systems & Cyber Security",
            "5": "Tren Populer IT Del",
        },
        "Teknologi Informasi": {
            "1": "Full-Stack Web & Mobile Development",
            "2": "Cloud Systems & DevOps Engineering",
            "3": "Database Administration & Big Data",
            "4": "Web Security & Vulnerability Assessment",
            "5": "UI/UX & AI Application Integration",
        },
        "D4 Teknologi Rekayasa Perangkat Lunak": {
            "1": "Applied Software Architecture & Microservices",
            "2": "Event-Driven Architecture & CQRS",
            "3": "API Gateway & High-Performance gRPC",
            "4": "DevOps, CI/CD, & Kubernetes",
            "5": "Tren Populer IT Del",
        },
        "D3 Teknologi Komputer": {
            "1": "IoT & Smart Sensor Networks",
            "2": "Network Engineering & Cyber Security (Cisco/Firewall)",
            "3": "Microcontroller & Embedded Systems (ESP32/Arduino)",
            "4": "Edge AI & TinyML Robotics",
            "5": "Server Administration & Linux Cloud",
        },
        "D3 Teknologi Informasi": {
            "1": "Full-Stack Web & Mobile Application Development",
            "2": "E-Commerce & Database Administration",
            "3": "Interactive UI/UX & Human-Computer Interaction",
            "4": "Applied Web Security",
            "5": "Tren Populer IT Del",
        },
    }

    @classmethod
    def _infer_topic_from_selection(cls, query: str, prodi: str) -> Optional[str]:
        query_clean = query.strip().lower()
        if not prodi:
            return None

        selection_map = cls.PRODI_SELECTION_TOPICS.get(prodi, {})
        if not selection_map:
            return None

        number_match = re.match(r'^(?:nomor\s*)?([1-5])(?:\.|\s|$)', query_clean)
        if number_match:
            return selection_map.get(number_match.group(1))

        for topic in selection_map.values():
            topic_lc = topic.lower()
            if topic_lc in query_clean:
                return topic
            topic_words = [w for w in re.findall(r'[a-z0-9]+', topic_lc) if len(w) > 2]
            if any(w in query_clean for w in topic_words):
                return topic

        return None

    @classmethod
    def evaluate(cls, query: str, conversation_history: str = "", session_prodi: str = "") -> Dict[str, Any]:
        query_clean = query.strip().lower()
        combined_text = (query + " " + conversation_history).lower()

        state = InterviewState()

        # 1. Deteksi Prodi: Pahami KUERI PENGGUNA SAAT INI TERLEBIH DAHULU (Current Query Precedence)
        is_generic_thesis_request = any(phrase in query_clean for phrase in ["bantu saya cari ide", "cari ide skripsi", "berikan ide skripsi", "rekomendasi ide skripsi", "tugas akhir"])
        
        # Cari prodi di kueri pengguna saat ini terlebih dahulu
        for kw, p_name in cls.PRODI_MAP.items():
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, query_clean):
                state.prodi = p_name
                info = cls.PROGRAM_STUDI[p_name]
                state.jenjang = info["jenjang"]
                state.fakultas = info["fakultas"]
                break

        # Utamakan session_prodi jika prodi tidak ada di kueri saat ini
        if not state.prodi and session_prodi and session_prodi in cls.PROGRAM_STUDI:
            state.prodi = session_prodi
            info = cls.PROGRAM_STUDI[session_prodi]
            state.jenjang = info["jenjang"]
            state.fakultas = info["fakultas"]

        # Jika masih tidak ditemukan, baru periksa riwayat lama
        if not state.prodi and not is_generic_thesis_request:
            last_prodi_match = None
            max_position = -1
            for kw, p_name in cls.PRODI_MAP.items():
                pattern = r'\b' + re.escape(kw) + r'\b'
                matches = list(re.finditer(pattern, conversation_history.lower()))
                if matches:
                    last_match_end = matches[-1].end()
                    if last_match_end > max_position:
                        max_position = last_match_end
                        last_prodi_match = p_name

            if last_prodi_match:
                state.prodi = last_prodi_match
                info = cls.PROGRAM_STUDI[last_prodi_match]
                state.jenjang = info["jenjang"]
                state.fakultas = info["fakultas"]

        # 2. Cek Apakah Menu Pernah Diberikan di Percakapan Sebelumnya
        if any(marker in conversation_history.lower() for marker in ["pilihan mana", "kategori", "1.", "2.", "3."]):
            state.has_menu_been_presented = True

        # 3. Deteksi Topik / Pilihan Menu dengan Exact & Word Boundary Matching
        if state.has_menu_been_presented:
            selection_topic = cls._infer_topic_from_selection(query_clean, state.prodi)
            if selection_topic:
                state.topic = selection_topic
            elif query_clean in cls.TOPIC_MAP:
                state.topic = cls.TOPIC_MAP[query_clean]
            else:
                for kw, t_name in cls.TOPIC_MAP.items():
                    if kw not in ["1", "2", "3", "4", "5"]:
                        pattern = r'\b' + re.escape(kw) + r'\b'
                        if re.search(pattern, combined_text):
                            state.topic = t_name
                            break
        else:
            for kw, t_name in cls.TOPIC_MAP.items():
                if kw not in ["1", "2", "3", "4", "5"]:
                    pattern = r'\b' + re.escape(kw) + r'\b'
                    if re.search(pattern, combined_text):
                        state.topic = t_name
                        break

        # 3b. Fallback Smart Topic Detection: Jika prodi terdeteksi dan pengguna menyebutkan 'bebas' atau kata 'tentang'
        if state.prodi and not state.topic:
            if any(phrase in query_clean for phrase in ["bebas", "kamu yang pilih", "terserah", "pilihkan"]):
                UNIVERSAL_PRODI_DEFAULT_TOPICS = {
                    "Teknik Bioproses": "Bioprocess Simulation & Fermentation Control",
                    "Bioteknologi": "Bioinformatics & Molecular Data Mining",
                    "Teknik Elektro": "Sistem Kontrol & Otomasi Industri",
                    "Teknik Metalurgi": "Mineral Processing & Metallurgy Analytics",
                    "Manajemen Rekayasa": "Supply Chain Management & Logistics",
                    "Sistem Informasi": "Business Process Re-engineering & BI Dashboards",
                    "Informatika": "Advanced AI & Natural Language Processing",
                    "Teknologi Informasi": "Full-Stack Web & Cloud Systems",
                    "D4 Teknologi Rekayasa Perangkat Lunak": "Applied Software Architecture & Microservices",
                    "D3 Teknologi Komputer": "IoT & Embedded Systems Networks",
                    "D3 Teknologi Informasi": "Applied Web & Mobile Application Development"
                }
                state.topic = UNIVERSAL_PRODI_DEFAULT_TOPICS.get(state.prodi, f"Kajian Riset Utama {state.prodi}")
            else:
                topic_trigger_keywords = ["tentang", "bertema", "mengenai", "topik", "skripsi", "ta", "microservices", "software", "aplikasi", "sistem", "arsitektur", "pengembangan", "kontrol", "otomasi", "listrik", "robotik", "fermentasi", "bioreaktor", "enzim"]
                if any(kw in query_clean for kw in topic_trigger_keywords):
                    # Infer topic based on query contents
                    if "bioproses" in query_clean or "fermentasi" in query_clean or "bioreaktor" in query_clean:
                        state.topic = "Bioprocess Simulation & Fermentation Control"
                    elif "microservice" in query_clean or "software" in query_clean or "rekayasa" in query_clean or "vokasi" in query_clean:
                        state.topic = "Applied Software Development"
                    elif "data" in query_clean or "analytics" in query_clean or "bi" in query_clean:
                        state.topic = "Data Analytics & BI"
                    elif "supply" in query_clean or "manufaktur" in query_clean or "industri" in query_clean:
                        state.topic = "Supply Chain & Logistics"
                    elif "elektro" in query_clean or "kontrol" in query_clean or "otomasi" in query_clean or "robot" in query_clean:
                        state.topic = "Control Systems & Automation"
                    else:
                        state.topic = "AI & Smart Systems"

        # 4. State Machine Transition Logic
        if state.prodi and state.topic:
            print(f"[INTERVIEW PLANNER] State: READY (Prodi={state.prodi}, Fakultas={state.fakultas}, Jenjang={state.jenjang}, Topic={state.topic})")
            return {
                "state": "ready",
                "missing": [],
                "next_action": "generate",
                "is_complete": True,
                "clarification": "",
                "metadata": {
                    "prodi": state.prodi,
                    "fakultas": state.fakultas,
                    "jenjang": state.jenjang,
                    "topic": state.topic
                }
            }

        if state.prodi and not state.topic:
            print(f"[INTERVIEW PLANNER] State: COLLECT_TOPIC (Prodi={state.prodi}, Fakultas={state.fakultas})")
            
            # Rekomendasi Kategori Otomatis Berdasarkan 10 Prodi IT Del
            PRODI_CATEGORIES = {
                "Teknik Bioproses": "1. Bioprocess Simulation & Fermentation Control, 2. Bioreactor Modeling & Kinetics, 3. Biomass & Bioresource Analytics, 4. Enzyme & Downstream Processing, 5. Tren Populer IT Del",
                "Bioteknologi": "1. Bioinformatics & Molecular Data Mining, 2. Genomic Sequence Analytics, 3. Industrial Biotechnology, 4. Medical & Agricultural Biotech, 5. Tren Populer IT Del",
                "Teknik Elektro": "1. Sistem Kontrol & Otomasi Industri, 2. Power Systems & Renewable Energy, 3. Signal Processing & Robotics, 4. Embedded Systems & IoT, 5. Tren Populer IT Del",
                "Teknik Metalurgi": "1. Mineral Processing & Flotation Analytics, 2. Pyrometallurgy & Hydrometallurgy Modeling, 3. Corrosion Analytics & Material Degradation, 4. Extractive Metallurgy, 5. Tren Populer IT Del",
                "Manajemen Rekayasa": "1. Supply Chain Management & Logistics, 2. Quality Control & Six Sigma (DMAIC), 3. Industrial Process Optimization, 4. Operations Research & Inventory Systems, 5. Tren Populer IT Del",
                "Sistem Informasi": "1. Business Process Re-engineering & BPMN, 2. Enterprise Systems (ERP Odoo/CRM), 3. Business Intelligence & BI Dashboards, 4. IT Governance & Audit (ITIL/COBIT), 5. AI & Smart Information Systems",
                "Informatika": "1. Advanced AI & Deep Learning, 2. Natural Language Processing & RAG, 3. Computer Vision & Image Analytics, 4. Distributed Systems & Cyber Security, 5. Tren Populer IT Del",
                "Teknologi Informasi": "1. Full-Stack Web & Mobile Development, 2. Cloud Systems & DevOps Engineering, 3. Database Administration & Big Data, 4. Web Security & Vulnerability Assessment, 5. UI/UX & AI Application Integration",
                "D4 Teknologi Rekayasa Perangkat Lunak": "1. Applied Software Architecture & Microservices, 2. Event-Driven Architecture & CQRS, 3. API Gateway & High-Performance gRPC, 4. DevOps, CI/CD, & Kubernetes, 5. Tren Populer IT Del",
                "D3 Teknologi Komputer": "1. IoT & Smart Sensor Networks, 2. Network Engineering & Cyber Security (Cisco/Firewall), 3. Microcontroller & Embedded Systems (ESP32/Arduino), 4. Edge AI & TinyML Robotics, 5. Server Administration & Linux Cloud",
                "D3 Teknologi Informasi": "1. Full-Stack Web & Mobile Application Development, 2. E-Commerce & Database Administration, 3. Interactive UI/UX & Human-Computer Interaction, 4. Applied Web Security, 5. Tren Populer IT Del"
            }

            category_text = PRODI_CATEGORIES.get(
                state.prodi,
                "1. AI & Smart Systems, 2. Data Analytics & BI, 3. Enterprise Systems, 4. Domain Specific Analytics, 5. Tren Populer IT Del"
            )

            return {
                "state": "collect_topic",
                "missing": ["topic"],
                "next_action": "ask_topic",
                "is_complete": False,
                "clarification": f"Untuk prodi {state.prodi} ({state.fakultas} - {state.jenjang}), pilihan mana yang Anda minati: {category_text} (atau sebutkan mata kuliah favorit Anda)?"
            }

        print("[INTERVIEW PLANNER] State: COLLECT_PRODI")
        return {
            "state": "collect_prodi",
            "missing": ["prodi", "topic"],
            "next_action": "ask_prodi",
            "is_complete": False,
            "clarification": "Halo! Boleh tahu Program Studi Anda di IT Del (misal: Sistem Informasi, Informatika, D4 TRPL, atau Manajemen Rekayasa)?"
        }


def check_information_completeness(query: str, conversation_history: str = "", session_prodi: str = "") -> dict:
    """
    Wrapper fungsi legasi agar tetap kompatibel 100% dengan RAG pipeline.
    """
    return InterviewPlanner.evaluate(query, conversation_history, session_prodi=session_prodi)
