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

    return text


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
    # RETURN STRUCTURED EVIDENCE
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
        )
    }