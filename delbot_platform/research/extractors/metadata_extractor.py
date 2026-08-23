from delbot_platform.research.utils.extraction_utils import (
    extract_canonical_technologies,
    extract_canonical_methodologies,
    extract_canonical_datasets,
    extract_canonical_metrics,
    extract_canonical_domains
)

# =====================================
# TECHNOLOGY EXTRACTOR
# =====================================
def extract_technologies(text: str) -> list:
    technologies = []
    for tech, _ in extract_canonical_technologies(text):
        technologies.append(tech)
    return sorted(list(set(technologies)))

def update_technology_counter(counter, text: str):
    for tech in extract_technologies(text):
        counter[tech] += 1

# =====================================
# METHODOLOGY EXTRACTOR
# =====================================
def extract_methodologies(text: str) -> list:
    methodologies = []
    for method, _ in extract_canonical_methodologies(text):
        methodologies.append(method)
    return sorted(list(set(methodologies)))

def update_methodology_counter(counter, text: str):
    for method in extract_methodologies(text):
        counter[method] += 1

# =====================================
# DATASET EXTRACTOR
# =====================================
def extract_datasets(text: str) -> list:
    datasets = []
    for dataset, _ in extract_canonical_datasets(text):
        datasets.append(dataset)
    return sorted(list(set(datasets)))

def update_dataset_counter(counter, text: str):
    for dataset in extract_datasets(text):
        counter[dataset] += 1

# =====================================
# METRIC EXTRACTOR
# =====================================
def extract_metrics(text: str) -> list:
    metrics = []
    for metric, _ in extract_canonical_metrics(text):
        metrics.append(metric)
    return sorted(list(set(metrics)))

def update_metric_counter(counter, text: str):
    for metric in extract_metrics(text):
        counter[metric] += 1

# =====================================
# DOMAIN EXTRACTOR
# =====================================
def extract_domains(text: str) -> list:
    domains = []
    for domain, _ in extract_canonical_domains(text):
        domains.append(domain)
    return sorted(list(set(domains)))

def update_domain_counter(counter, text: str):
    for domain in extract_domains(text):
        counter[domain] += 1
