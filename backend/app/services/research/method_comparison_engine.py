import re

from collections import Counter

from app.services.llm.model_gateway import (
    gateway
)

# =====================================
# COMPARE KEYWORDS
# =====================================

COMPARE_KEYWORDS = [

    "bandingkan",

    "perbandingan",

    "compare",

    "versus",

    "vs",

    "lebih baik"
]

# =====================================
# METHOD CANDIDATES
# =====================================

METHOD_CANDIDATES = [

    "cnn",

    "svm",

    "random forest",

    "xgboost",

    "decision tree",

    "transformer",

    "bert",

    "lstm",

    "gru",

    "mobilenet",

    "resnet",

    "yolo",

    "tensorflow",

    "pytorch",

    "naive bayes",

    "k nearest neighbor",

    "knn"
]

# =====================================
# NORMALIZE
# =====================================

def normalize_text(
    text: str
):

    if not text:
        return ""

    return text.lower().strip()

# =====================================
# DETECT COMPARISON QUERY
# =====================================

def is_comparison_query(
    query: str
):

    query = normalize_text(query)

    return any(

        keyword in query

        for keyword

        in COMPARE_KEYWORDS
    )

# =====================================
# EXTRACT METHODS
# =====================================

def extract_methods(
    query: str
):

    query = normalize_text(query)

    found = []

    for method in METHOD_CANDIDATES:

        pattern = rf"\b{re.escape(method)}\b"

        if re.search(
            pattern,
            query,
            flags=re.IGNORECASE
        ):
            found.append(method)

    return found[:2]

# =====================================
# METHOD STATISTICS
# =====================================

def build_method_statistics(
    method: str,
    theses: list
):

    matched = []

    domain_counter = Counter()

    dataset_counter = Counter()

    metric_counter = Counter()

    years = []

    for thesis in theses:

        title = thesis.get(
            "title",
            ""
        ) or ""

        abstract = thesis.get(
            "abstract",
            ""
        ) or ""

        chunk = thesis.get(
            "chunk",
            ""
        ) or ""

        text = normalize_text(

            f"""
            {title}
            {abstract}
            {chunk}
            """
        )

        if method not in text:
            continue

        matched.append(
            thesis
        )

        year = thesis.get(
            "year"
        )

        if year:
            years.append(
                str(year)
            )

        domain = thesis.get(
            "prodi"
        )

        if domain:

            domain_counter[
                domain
            ] += 1

        for dataset in [

            "mnist",

            "cifar",

            "imdb",

            "twitter",

            "custom dataset",

            "dataset mahasiswa"
        ]:

            if dataset in text:

                dataset_counter[
                    dataset
                ] += 1

        for metric in [

            "accuracy",

            "precision",

            "recall",

            "f1-score",

            "auc",

            "mae",

            "rmse"
        ]:

            if metric in text:

                metric_counter[
                    metric
                ] += 1

    return {

        "method":
        method,

        "frequency":
        len(matched),

        "years":
        sorted(
            list(set(years))
        ),

        "domains":
        [

            item[0]

            for item

            in domain_counter.most_common(5)
        ],

        "datasets":
        [

            item[0]

            for item

            in dataset_counter.most_common(5)
        ],

        "evaluation_metrics":
        [

            item[0]

            for item

            in metric_counter.most_common(5)
        ]
    }

# =====================================
# BUILD COMPARISON MATRIX
# =====================================

def build_comparison_matrix(
    methods: list,
    theses: list
):

    matrix = {}

    for method in methods:

        matrix[
            method
        ] = build_method_statistics(
            method,
            theses
        )

    return matrix

# =====================================
# COMPARISON PROMPT
# =====================================

def build_comparison_prompt(
    query: str,
    matrix: dict
):

    return f"""
Anda adalah DELBot.

Asisten riset akademik.

==================================================
PERTANYAAN
==================================================

{query}

==================================================
DATA PERBANDINGAN
==================================================

{matrix}

==================================================
TUGAS
==================================================

Bandingkan seluruh metode berdasarkan:

1. Frekuensi penggunaan
2. Domain penelitian
3. Dataset yang digunakan
4. Metrik evaluasi
5. Tren penelitian
6. Kelebihan
7. Kekurangan
8. Rekomendasi penggunaan

==================================================
ATURAN
==================================================

1. Gunakan Bahasa Indonesia formal.

2. Gunakan hanya data yang tersedia.

3. Jangan mengarang dataset.

4. Jangan mengarang frekuensi.

5. Jika data kurang,
   katakan data tidak mencukupi.

==================================================
FORMAT
==================================================

# Ringkasan

# Tabel Perbandingan

# Analisis Metode

# Kelebihan dan Kekurangan

# Rekomendasi
"""

# =====================================
# MAIN ENGINE
# =====================================

def run_method_comparison(
    query: str,
    theses: list
):

    methods = extract_methods(
        query
    )

    if len(methods) < 2:

        return {

            "mode":
            "comparison",

            "comparison":
            "Minimal dua metode diperlukan.",

            "comparison_matrix":
            {},

            "methods":
            methods
        }

    matrix = build_comparison_matrix(

        methods,

        theses
    )

    prompt = build_comparison_prompt(

        query=query,

        matrix=matrix
    )

    analysis = gateway.generate_response(
        prompt=prompt
    )

    return {

        "mode":
        "comparison",

        "methods":
        methods,

        "comparison_matrix":
        matrix,

        "comparison":
        analysis
    }