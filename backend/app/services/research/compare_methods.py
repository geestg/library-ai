from collections import Counter


# =====================================
# METHOD KNOWLEDGE BASE
# =====================================

METHOD_KNOWLEDGE = {

    "svm": {

        "interpretability":
        "Sedang",

        "complexity":
        "Sedang",

        "advantages": [

            "Baik untuk dataset berukuran kecil hingga menengah",

            "Performa stabil pada klasifikasi",

            "Efektif pada data berdimensi tinggi"
        ],

        "limitations": [

            "Kurang efisien pada dataset sangat besar",

            "Sensitif terhadap pemilihan parameter"
        ],

        "recommended_scenarios": [

            "Text Classification",

            "Sentiment Analysis",

            "Medical Classification"
        ]
    },

    "random forest": {

        "interpretability":
        "Tinggi",

        "complexity":
        "Sedang",

        "advantages": [

            "Robust terhadap overfitting",

            "Mudah digunakan",

            "Dapat menangani fitur yang banyak"
        ],

        "limitations": [

            "Ukuran model besar",

            "Kurang optimal untuk data sangat kompleks"
        ],

        "recommended_scenarios": [

            "Prediction",

            "Classification",

            "Decision Support System"
        ]
    },

    "xgboost": {

        "interpretability":
        "Rendah",

        "complexity":
        "Tinggi",

        "advantages": [

            "Akurasi tinggi",

            "Performa sangat baik pada tabular data",

            "Mendukung regularisasi"
        ],

        "limitations": [

            "Konfigurasi lebih kompleks",

            "Interpretasi model lebih sulit"
        ],

        "recommended_scenarios": [

            "Prediction",

            "Fraud Detection",

            "Risk Analysis"
        ]
    },

    "cnn": {

        "interpretability":
        "Rendah",

        "complexity":
        "Tinggi",

        "advantages": [

            "Sangat baik untuk citra",

            "Feature extraction otomatis",

            "Akurasi tinggi pada Computer Vision"
        ],

        "limitations": [

            "Butuh dataset besar",

            "Biaya komputasi tinggi"
        ],

        "recommended_scenarios": [

            "Image Classification",

            "Object Detection",

            "Medical Imaging"
        ]
    },

    "bert": {

        "interpretability":
        "Rendah",

        "complexity":
        "Tinggi",

        "advantages": [

            "Memahami konteks bahasa",

            "Sangat baik untuk NLP",

            "Mendukung transfer learning"
        ],

        "limitations": [

            "Resource intensive",

            "Fine tuning cukup mahal"
        ],

        "recommended_scenarios": [

            "NLP",

            "Question Answering",

            "Sentiment Analysis"
        ]
    }
}


# =====================================
# EXTRACT METHOD FREQUENCY
# =====================================

def extract_method_frequency(
    evidence_matrix: dict
):

    return evidence_matrix.get(
        "technology_frequency",
        {}
    )


# =====================================
# BUILD COMPARISON ENTRY
# =====================================

def build_method_entry(

    method_name: str,

    frequency: int

):

    metadata = METHOD_KNOWLEDGE.get(

        method_name.lower(),

        {

            "interpretability":
            "Tidak diketahui",

            "complexity":
            "Tidak diketahui",

            "advantages": [],

            "limitations": [],

            "recommended_scenarios": []
        }
    )

    return {

        "method":
        method_name,

        "frequency":
        frequency,

        "interpretability":
        metadata[
            "interpretability"
        ],

        "complexity":
        metadata[
            "complexity"
        ],

        "advantages":
        metadata[
            "advantages"
        ],

        "limitations":
        metadata[
            "limitations"
        ],

        "recommended_scenarios":
        metadata[
            "recommended_scenarios"
        ]
    }


# =====================================
# COMPARE METHODS
# =====================================

def compare_methods(
    evidence_matrix: dict
):

    method_frequency = (
        extract_method_frequency(
            evidence_matrix
        )
    )

    if not method_frequency:

        return {

            "summary":
            "Tidak ditemukan metode yang cukup untuk dibandingkan.",

            "methods":
            []
        }

    comparison = []

    sorted_methods = sorted(

        method_frequency.items(),

        key=lambda x: x[1],

        reverse=True
    )

    for method_name, frequency in sorted_methods:

        comparison.append(

            build_method_entry(

                method_name,

                frequency
            )
        )

    dominant_method = (
        sorted_methods[0][0]
    )

    summary = f"""
Metode yang paling sering muncul
dalam hasil retrieval adalah
{dominant_method}.

Perbandingan dilakukan berdasarkan
frekuensi kemunculan, kompleksitas,
interpretabilitas, kelebihan,
kekurangan, dan skenario penggunaan.
"""

    return {

        "summary":
        summary.strip(),

        "methods":
        comparison
    }


# =====================================
# MARKDOWN TABLE
# =====================================

def build_comparison_table(
    comparison_result: dict
):

    methods = comparison_result.get(
        "methods",
        []
    )

    if not methods:

        return (
            "Tidak ada metode yang "
            "dapat dibandingkan."
        )

    lines = []

    lines.append(
        "| Method | Frequency | Interpretability | Complexity |"
    )

    lines.append(
        "|----------|----------|----------|----------|"
    )

    for item in methods:

        lines.append(

            f"| {item['method']} "

            f"| {item['frequency']} "

            f"| {item['interpretability']} "

            f"| {item['complexity']} |"
        )

    return "\n".join(lines)