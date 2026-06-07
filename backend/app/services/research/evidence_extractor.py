import re

from collections import Counter


# =====================================
# HIGH CONFIDENCE TECHNOLOGIES
# =====================================

HIGH_CONFIDENCE_TECHNOLOGIES = [

    "laravel",
    "odoo",
    "api",
    "web service",
    "web services",
    "soa",
    "dashboard",
    "website",
    "php",
    "java",
    "python",
    "mysql",
    "postgresql"
]


# =====================================
# LOW CONFIDENCE TECHNOLOGIES
# =====================================

LOW_CONFIDENCE_TECHNOLOGIES = [

    "cnn",
    "svm",
    "bert",
    "transformer",
    "lstm",
    "gru",
    "mobilenet",
    "resnet",
    "yolo",
    "tensorflow",
    "pytorch",
    "random forest",
    "xgboost",
    "decision tree"
]


# =====================================
# HIGH CONFIDENCE METHODOLOGIES
# =====================================

HIGH_CONFIDENCE_METHODOLOGIES = [

    "waterfall",
    "sdlc",
    "black box",
    "white box",
    "design pattern",
    "qualitative",
    "quantitative",
    "deskriptif",
    "descriptive"
]


# =====================================
# LOW CONFIDENCE METHODOLOGIES
# =====================================

LOW_CONFIDENCE_METHODOLOGIES = [

    "mvc",
    "agile",
    "scrum",
    "prototype",
    "prototyping",
    "spiral",
    "rad",
    "transfer learning",
    "cross validation",
    "k-fold"
]


# =====================================
# RESEARCH DOMAINS
# =====================================

DOMAIN_PATTERNS = [

    "penerimaan mahasiswa baru",
    "pmb",
    "spmb",
    "dashboard",
    "sistem informasi",
    "machine learning",
    "deep learning",
    "computer vision",
    "natural language processing",
    "nlp",
    "sentiment analysis",
    "internet of things",
    "iot",
    "cyber security",
    "blockchain",
    "recommender system"
]


# =====================================
# DATASETS
# =====================================

DATASET_PATTERNS = [

    "mnist",
    "fashion-mnist",
    "cifar",
    "cifar10",
    "cifar-10",
    "imagenet",
    "coco",
    "pascal voc",
    "kdd",
    "nsl-kdd",
    "unsw-nb15",
    "iris",
    "uci",
    "kaggle"
]


# =====================================
# EVALUATION METRICS
# =====================================

METRIC_PATTERNS = [

    "accuracy",
    "precision",
    "recall",
    "f1",
    "f1-score",
    "auc",
    "roc",
    "specificity",
    "sensitivity",
    "mae",
    "mse",
    "rmse",
    "r2",
    "mean absolute error",
    "mean squared error",
    "confusion matrix"
]


# =====================================
# NORMALIZE TEXT
# =====================================

def normalize_text(
    text: str
):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================
# SAFE TERM MATCHING
# =====================================

def contains_term(

    text: str,

    term: str

):

    pattern = rf"\b{re.escape(term)}\b"

    return bool(

        re.search(

            pattern,

            text,

            flags=re.IGNORECASE
        )
    )


# =====================================
# TITLE KEYWORDS
# =====================================

def extract_keywords_from_title(
    title: str
):

    if not title:

        return []

    stopwords = {

        "dan",
        "dengan",
        "untuk",
        "yang",
        "dalam",
        "berbasis",
        "studi",
        "kasus",
        "implementasi",
        "rancang",
        "bangun",
        "sistem",
        "informasi",
        "analisis",
        "pengembangan",
        "penerapan",
        "pada"
    }

    words = re.findall(

        r"[a-zA-Z]+",

        title.lower()
    )

    words = [

        word

        for word in words

        if len(word) > 3

        and word not in stopwords
    ]

    return words


# =====================================
# FORMAT COUNTER
# =====================================

def counter_to_structured_list(
    counter: Counter
):

    return [

        {
            "name": name,
            "count": count
        }

        for name, count

        in counter.most_common()
    ]


# =====================================
# EXTRACT EVIDENCE
# =====================================

def extract_evidence(
    theses: list
):

    technology_counter = Counter()

    methodology_counter = Counter()

    keyword_counter = Counter()

    domain_counter = Counter()

    dataset_counter = Counter()

    metric_counter = Counter()

    year_counter = Counter()

    # =================================
    # ITERATE THESIS
    # =================================

    for thesis in theses:

        title = thesis.get(
            "title",
            ""
        )

        abstract = thesis.get(
            "abstract",
            ""
        )

        chunk = thesis.get(
            "chunk",
            ""
        )

        year = thesis.get(
            "year"
        )

        text = normalize_text(

            f"{title}\n{abstract}\n{chunk}"
        )

        # =============================
        # TECHNOLOGIES
        # =============================

        for tech in HIGH_CONFIDENCE_TECHNOLOGIES:

            if contains_term(
                text,
                tech
            ):

                technology_counter[
                    tech
                ] += 1

        for tech in LOW_CONFIDENCE_TECHNOLOGIES:

            occurrences = len(

                re.findall(

                    rf"\b{re.escape(tech)}\b",

                    text,

                    flags=re.IGNORECASE
                )
            )

            if occurrences >= 2:

                technology_counter[
                    tech
                ] += occurrences

        # =============================
        # METHODOLOGIES
        # =============================

        for method in HIGH_CONFIDENCE_METHODOLOGIES:

            if contains_term(
                text,
                method
            ):

                methodology_counter[
                    method
                ] += 1

        for method in LOW_CONFIDENCE_METHODOLOGIES:

            occurrences = len(

                re.findall(

                    rf"\b{re.escape(method)}\b",

                    text,

                    flags=re.IGNORECASE
                )
            )

            if occurrences >= 2:

                methodology_counter[
                    method
                ] += occurrences

        # =============================
        # DOMAINS
        # =============================

        for domain in DOMAIN_PATTERNS:

            if contains_term(
                text,
                domain
            ):

                domain_counter[
                    domain
                ] += 1

        # =============================
        # DATASETS
        # =============================

        for dataset in DATASET_PATTERNS:

            if contains_term(
                text,
                dataset
            ):

                dataset_counter[
                    dataset
                ] += 1

        # =============================
        # METRICS
        # =============================

        for metric in METRIC_PATTERNS:

            if contains_term(
                text,
                metric
            ):

                metric_counter[
                    metric
                ] += 1

        # =============================
        # YEARS
        # =============================

        if year:

            year_counter[
                str(year)
            ] += 1

        # =============================
        # KEYWORDS
        # =============================

        title_keywords = (
            extract_keywords_from_title(
                title
            )
        )

        for keyword in title_keywords:

            keyword_counter[
                keyword
            ] += 1

    # =================================
    # DEBUG
    # =================================

    print("\n")
    print("=" * 80)
    print("COUNTER DEBUG")
    print("=" * 80)

    print(
        "TECH:",
        technology_counter
    )

    print(
        "METHOD:",
        methodology_counter
    )

    print(
        "DOMAIN:",
        domain_counter
    )

    print(
        "DATASET:",
        dataset_counter
    )

    print(
        "METRIC:",
        metric_counter
    )

    print(
        "YEAR:",
        year_counter
    )

    print(
        "KEYWORD:",
        keyword_counter
    )

    # =================================
    # RETURN
    # =================================

    return {

        "technologies":

        counter_to_structured_list(
            technology_counter
        ),

        "methodologies":

        counter_to_structured_list(
            methodology_counter
        ),

        "keywords":

        counter_to_structured_list(
            keyword_counter
        ),

        "research_domains":

        counter_to_structured_list(
            domain_counter
        ),

        "datasets":

        counter_to_structured_list(
            dataset_counter
        ),

        "evaluation_metrics":

        counter_to_structured_list(
            metric_counter
        ),

        "years":

        counter_to_structured_list(
            year_counter
        )
    }