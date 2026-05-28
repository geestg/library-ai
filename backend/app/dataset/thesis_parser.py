import json


def load_dataset(path: str):

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data