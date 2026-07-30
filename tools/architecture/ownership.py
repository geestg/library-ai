from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


REPORTS = Path(__file__).resolve().parents[2] / "reports"


def load_json(name: str):

    path = REPORTS / name

    with path.open(
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


def detect_layer(path: str) -> str:

    parts = Path(path).parts

    candidates = {
        "ai",
        "api",
        "application",
        "boot",
        "config",
        "controller",
        "core",
        "document_intelligence",
        "documents",
        "gateway",
        "knowledge",
        "launcher",
        "orchestrator",
        "repository",
        "research",
        "vectorstore",
        "vectors",
        "workspace",
        "workflows",
    }

    for part in parts:

        if part in candidates:
            return part

    return "other"


def detect_component(path: str) -> str:

    name = Path(path).stem.lower()

    if "service" in name:
        return "service"

    if "builder" in name:
        return "builder"

    if "factory" in name:
        return "factory"

    if "pipeline" in name:
        return "pipeline"

    if "parser" in name:
        return "parser"

    if "loader" in name:
        return "loader"

    if "model" in name:
        return "model"

    if "mapper" in name:
        return "mapper"

    if "registry" in name:
        return "registry"

    if "retriever" in name:
        return "retriever"

    if "rerank" in name:
        return "reranker"

    return "module"


def main():

    inventory = load_json(
        "architecture_inventory.json",
    )

    dependency = load_json(
        "architecture_dependency.json",
    )

    dependency_map = {}

    incoming = defaultdict(int)

    for module in dependency["modules"]:

        dependency_map[module["module"]] = module["imports"]

        for target in module["imports"]:

            incoming[target] += 1

    rows = []

    for item in inventory:

        relative = item["relative_path"]

        module = (
            relative
            .replace("/", ".")
            .replace("\\", ".")
            .replace(".py", "")
        )

        outgoing = dependency_map.get(
            module,
            [],
        )

        rows.append({

            "module": module,

            "path": relative,

            "layer": detect_layer(relative),

            "component": detect_component(relative),

            "incoming": incoming.get(module, 0),

            "outgoing": len(outgoing),

            "classes": len(item["classes"]),

            "functions": len(item["functions"]),

            "async_functions": len(item["async_functions"]),

            "lines": item["lines"],

            "size": item["size"],

        })

    ############################################################

    with (REPORTS / "architecture_ownership.json").open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            rows,
            fp,
            indent=4,
        )

    ############################################################

    with (REPORTS / "architecture_ownership.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.DictWriter(
            fp,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()

        writer.writerows(rows)

    ############################################################

    summary = []

    summary.append("# DELBot Architecture Ownership")
    summary.append("")
    summary.append("## Summary")
    summary.append("")
    summary.append(f"Modules : {len(rows)}")
    summary.append("")

    layers = defaultdict(int)

    for row in rows:

        layers[row["layer"]] += 1

    summary.append("| Layer | Modules |")
    summary.append("|--------|---------|")

    for layer in sorted(layers):

        summary.append(
            f"| {layer} | {layers[layer]} |"
        )

    (REPORTS / "architecture_ownership.md").write_text(

        "\n".join(summary),

        encoding="utf-8",

    )

    print()

    print("Ownership generated")

    print(f"Modules : {len(rows)}")

    print()


if __name__ == "__main__":
    main()
