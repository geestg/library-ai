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