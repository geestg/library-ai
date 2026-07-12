# =====================================
# DOMAIN KEYWORDS
# =====================================

DOMAIN_KEYWORDS = {

    "informatika": [

        "artificial intelligence",
        "ai",
        "machine learning",
        "deep learning",
        "computer vision",
        "nlp",
        "natural language processing",
        "transformer",
        "cnn",
        "yolo",
        "bert",
        "llm",
        "algoritma",
        "klasifikasi",
        "prediksi",
        "rekomendasi",
        "data mining"
    ],

    "sistem_informasi": [

        "sistem informasi",
        "erp",
        "crm",
        "it governance",
        "cobit",
        "audit ti",
        "keamanan informasi",
        "business process",
        "enterprise architecture",
        "data governance",
        "dashboard",
        "business intelligence"
    ],

    "trpl": [

        "software engineering",
        "rekayasa perangkat lunak",
        "microservice",
        "clean architecture",
        "devops",
        "software testing",
        "quality assurance",
        "requirement engineering",
        "enterprise system",
        "system design",
        "backend",
        "frontend"
    ],

    "teknologi_informasi": [

        "web development",
        "mobile application",
        "database",
        "api",
        "fullstack",
        "cloud application",
        "data analyst",
        "software development",
        "ui ux"
    ],

    "teknologi_komputer": [

        "iot",
        "internet of things",
        "embedded system",
        "mikrokontroler",
        "arduino",
        "esp32",
        "raspberry pi",
        "jaringan komputer",
        "cloud infrastructure",
        "network monitoring",
        "sensor"
    ],

    "teknik_elektro": [

        "sistem tenaga",
        "energi",
        "kelistrikan",
        "power system",
        "kontrol",
        "control system",
        "motor listrik",
        "elektronika",
        "plts",
        "smart grid",
        "instrumentasi"
    ],

    "manajemen_rekayasa": [

        "supply chain",
        "rantai pasok",
        "optimasi",
        "decision making",
        "pengambilan keputusan",
        "manajemen proyek",
        "analisis bisnis",
        "lean",
        "six sigma",
        "produktivitas",
        "risk management",
        "forecasting"
    ],

    "metalurgi": [

        "metalurgi",
        "ekstraksi logam",
        "mineral",
        "smelter",
        "korosi",
        "material",
        "alloy",
        "paduan",
        "perlakuan panas",
        "sifat mekanik",
        "baja",
        "nikel"
    ],

    "bioproses": [

        "bioproses",
        "fermentasi",
        "mikroorganisme",
        "biomassa",
        "bioetanol",
        "biogas",
        "enzim",
        "substrat",
        "yield",
        "bioreaktor",
        "kultur",
        "bakteri",
        "jamur"
    ]
}


# =====================================
# DETECT DOMAIN
# =====================================

def detect_domain(
    query: str
):

    q = query.lower()

    scores = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in q:

                score += 1

        scores[domain] = score

    best_domain = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_domain]

    if best_score == 0:

        return {

            "domain": "general",

            "confidence": 0.0
        }

    confidence = round(

        best_score /

        max(
            len(
                DOMAIN_KEYWORDS[
                    best_domain
                ]
            ),
            1
        ),

        2
    )

    return {

        "domain": best_domain,

        "confidence": confidence
    }

