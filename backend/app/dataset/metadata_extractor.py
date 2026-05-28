from typing import Dict


def extract_metadata(data: Dict):

    return {
        "title": data.get("title", ""),
        "author": data.get("author", ""),
        "year": data.get("year", ""),
        "department": data.get("department", ""),
        "abstract": data.get("abstract", ""),
        "keywords": data.get("keywords", []),
        "method": data.get("method", ""),
    }