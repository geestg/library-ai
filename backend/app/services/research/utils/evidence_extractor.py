import re
from collections import Counter


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

    words = title.lower().split()

    return [
        word.strip(".,:;()[]{}!?")
        for word in words
        if len(word.strip(".,:;()[]{}!?")) > 3
        and word.strip(".,:;()[]{}!?") not in stopwords
    ]


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
    domain_counter = Counter()
    dataset_counter = Counter()
    metric_counter = Counter()
    keyword_counter = Counter()
    year_counter = Counter()

    for thesis in theses:
        chunk_text = normalize_text(thesis.get("chunk", "") + " " + thesis.get("title", ""))

        # =============================
        # TECHNOLOGY
        # =============================
        # 0. Dynamic Grammatical Context-Pattern Triggers (Automatic Unseen Term Extractor)
        # Technology Trigger: "menggunakan/berbasis [Term]"
        tech_matches = re.findall(r'(?:menggunakan|berbasis|diimplementasikan dengan|memanfaatkan)\s+([A-Z][a-zA-Z0-9\-\+\.]+)', chunk_text)
        for t_match in tech_matches:
            if len(t_match) > 2 and t_match.lower() not in ["sistem", "metode", "aplikasi", "teknologi", "data"]:
                technology_counter[t_match.lower()] += 1

        # Methodology Trigger: "metode/metodologi/algoritma [Term]"
        method_matches = re.findall(r'(?:metode|metodologi|algoritma|pendekatan|framework)\s+([A-Z][a-zA-Z0-9\-\+\.]+)', chunk_text)
        for m_match in method_matches:
            if len(m_match) > 2 and m_match.lower() not in ["sistem", "pengembangan", "penelitian", "studi"]:
                methodology_counter[m_match.lower()] += 1

        # 1. Multi-Domain Technologies & Tools
        domain_tech_rules = {
            "bioprocess": ["bioreaktor", "fermentasi", "hplc", "pcr", "gc-ms", "enzim", "biomassa", "titrasi", "spektrofotometri", "sentrifugasi"],
            "metallurgy": ["leaching", "flotasi", "xrd", "sem-edx", "aas", "roasting", "pirometalurgi", "hidrometalurgi", "korosi", "smelting"],
            "industrial_eng": ["six sigma", "spc", "eoq", "slp", "simul8", "arena", "scor", "fmea", "kanban", "lean", "simulasi"],
            "electrical": ["plc", "scada", "pid", "matlab", "simulink", "etap", "mikrokontroler", "inverter", "fpga", "arduino", "esp32"],
            "software": ["laravel", "react", "python", "yolo", "bert", "rag", "docker", "kubernetes", "grpc", "kafka", "postgresql", "mysql"]
        }
        for domain_cat, tech_list in domain_tech_rules.items():
            for t_kw in tech_list:
                if re.search(r'\b' + re.escape(t_kw) + r'\b', chunk_text):
                    technology_counter[t_kw] += 1

        # 2. Multi-Domain Methodologies
        domain_method_rules = {
            "management": ["dmaic", "six sigma", "taguchi", "ahp", "topsis", "promethee", "scrum", "prototype", "sdlc", "waterfall"],
            "experimental": ["rsm", "response surface methodology", "factorial design", "doer", "trial and error"],
            "analytical": ["regression", "machine learning", "deep learning", "neural network", "simulation", "monte carlo"]
        }
        for m_cat, m_list in domain_method_rules.items():
            for m_kw in m_list:
                if re.search(r'\b' + re.escape(m_kw) + r'\b', chunk_text):
                    methodology_counter[m_kw] += 1

        # 3. Multi-Domain Datasets / Samples
        if "kuesioner" in chunk_text or "responden" in chunk_text:
            dataset_counter["data_kuesioner_responden"] += 1
        elif "sampel" in chunk_text or "ekstrak" in chunk_text:
            dataset_counter["sampel_laboratorium"] += 1
        elif "log" in chunk_text or "transaksi" in chunk_text:
            dataset_counter["log_transaksi_sistem"] += 1

        # 4. Multi-Domain Evaluation Metrics
        domain_metric_rules = ["precision", "recall", "f1-score", "ndcg", "mrr", "accuracy", "blackbox", "yield", "efisiensi", "error rate", "standard deviation", "p-value"]
        for met in domain_metric_rules:
            if re.search(r'\b' + re.escape(met) + r'\b', chunk_text):
                metric_counter[met] += 1

        # Standard Payload Metadata Check
        for technology in thesis.get("technologies", []):
            technology_counter[technology] += 1

        for methodology in thesis.get("methodologies", []):
            methodology_counter[methodology] += 1

        for domain in thesis.get("domains", []):
            domain_counter[domain] += 1

        for dataset in thesis.get("datasets", []):
            dataset_counter[dataset] += 1

        for metric in thesis.get("evaluation_metrics", []):
            metric_counter[metric] += 1

        # =============================
        # YEAR
        # =============================
        year = thesis.get(
            "year"
        )

        if year:
            year_counter[
                str(year)
            ] += 1

        # =============================
        # KEYWORDS
        # =============================
        title = thesis.get(
            "title",
            ""
        )

        for keyword in extract_keywords_from_title(
            title
        ):
            keyword_counter[
                keyword
            ] += 1

    print("\n")
    print("=" * 80)
    print("COUNTER DEBUG V4")
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