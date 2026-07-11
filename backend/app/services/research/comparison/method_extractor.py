import re

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


def normalize_text(
    text: str
):

    if not text:
        return ""

    return text.lower().strip()


def extract_methods(
    query: str
):

    query = normalize_text(
        query
    )

    found = []

    for method in METHOD_CANDIDATES:

        pattern = rf"\b{re.escape(method)}\b"

        if re.search(
            pattern,
            query,
            flags=re.IGNORECASE
        ):
            found.append(
                method
            )

    return found[:2]
