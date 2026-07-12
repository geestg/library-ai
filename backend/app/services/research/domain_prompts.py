DOMAIN_PROMPTS = {

    "informatika": """
Fokuskan analisis pada:

- algoritma
- machine learning
- artificial intelligence
- dataset
- evaluasi model
- performa model
- akurasi
- precision
- recall
- f1-score

Identifikasi peluang:
- model baru
- dataset baru
- optimasi performa
- perbandingan model
""",

    "sistem_informasi": """
Fokuskan analisis pada:

- proses bisnis
- tata kelola TI
- keamanan informasi
- integrasi sistem
- enterprise architecture
- business intelligence

Identifikasi peluang:
- optimasi proses bisnis
- transformasi digital
- tata kelola data
""",

    "trpl": """
Fokuskan analisis pada:

- software engineering
- software architecture
- testing
- maintainability
- scalability
- devops

Identifikasi peluang:
- desain sistem
- quality assurance
- engineering practice
""",

    "teknologi_informasi": """
Fokuskan analisis pada:

- pengembangan aplikasi
- database
- cloud
- web system
- mobile system

Identifikasi peluang:
- implementasi teknologi baru
- integrasi sistem
- peningkatan layanan digital
""",

    "teknologi_komputer": """
Fokuskan analisis pada:

- IoT
- embedded system
- jaringan komputer
- sensor
- cloud infrastructure

Identifikasi peluang:
- monitoring system
- smart device
- automation
""",

    "teknik_elektro": """
Fokuskan analisis pada:

- sistem tenaga listrik
- elektronika
- kontrol
- energi
- instrumentasi

Identifikasi peluang:
- efisiensi energi
- smart grid
- sistem kontrol cerdas
""",

    "manajemen_rekayasa": """
Fokuskan analisis pada:

- optimasi
- supply chain
- pengambilan keputusan
- produktivitas
- manajemen risiko

Identifikasi peluang:
- efisiensi proses
- optimasi biaya
- peningkatan kinerja organisasi
""",

    "metalurgi": """
Fokuskan analisis pada:

- ekstraksi logam
- pengolahan mineral
- korosi
- material
- paduan logam

Identifikasi peluang:
- material baru
- peningkatan sifat mekanik
- optimasi proses ekstraksi
""",

    "bioproses": """
Fokuskan analisis pada:

- fermentasi
- biomassa
- mikroorganisme
- bioreaktor
- yield produksi

Identifikasi peluang:
- optimasi substrat
- peningkatan yield
- efisiensi proses biokonversi
""",

    "general": """
Lakukan analisis akademik secara umum berdasarkan bukti penelitian yang tersedia.
"""
}


def get_domain_instruction(
    domain: str
):

    return DOMAIN_PROMPTS.get(
        domain,
        DOMAIN_PROMPTS["general"]
    )

