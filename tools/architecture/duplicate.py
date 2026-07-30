from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[2] / "reports"

# ============================================================================
# Ignore generic filenames.
# Mereka hampir selalu valid dan bukan duplicate arsitektur.
# ============================================================================

IGNORE_NAMES = {
    "__init__",
    "__main__",
    "base",
    "builder",
    "factory",
    "pipeline",
    "service",
    "services",
    "model",
    "models",
    "exceptions",
    "constant",
    "constants",
    "config",
    "types",
    "typing",
    "utils",
    "utility",
    "helpers",
    "helper",
    "common",
    "registry",
}

# ============================================================================

SUFFIXES = (
    "_service",
    "_services",
    "_builder",
    "_factory",
    "_pipeline",
    "_loader",
    "_parser",
    "_manager",
    "_registry",
    "_mapper",
    "_processor",
    "_handler",
    "_engine",
    "_client",
    "_provider",
    "_model",
)

# ============================================================================


def load_json(filename: str):

    with (REPORTS / filename).open(
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


# ============================================================================


def normalize(name: str):

    name = name.lower()

    for suffix in SUFFIXES:

        if name.endswith(suffix):

            name = name[:-len(suffix)]

            break

    return name


# ============================================================================


def should_ignore(name: str):

    return normalize(name) in IGNORE_NAMES


# ============================================================================


def build_groups(rows):

    groups = defaultdict(list)

    for row in rows:

        stem = Path(row["path"]).stem

        if should_ignore(stem):
            continue

        key = normalize(stem)

        groups[key].append(row)

    return groups


# ============================================================================


def classify(group):

    if len(group) < 2:
        return None

    layers = sorted({
        row["layer"]
        for row in group
    })

    components = sorted({
        row["component"]
        for row in group
    })

    incoming = sum(
        row["incoming"]
        for row in group
    )

    outgoing = sum(
        row["outgoing"]
        for row in group
    )

    return {

        "key": normalize(
            Path(group[0]["path"]).stem
        ),

        "count": len(group),

        "layers": layers,

        "components": components,

        "incoming": incoming,

        "outgoing": outgoing,

        "modules": sorted(
            row["module"]
            for row in group
        ),

        "paths": sorted(
            row["path"]
            for row in group
        ),
    }


# ============================================================================


def write_json(candidates):

    with (REPORTS / "duplicate_candidates.json").open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            candidates,
            fp,
            indent=4,
        )


# ============================================================================


def write_csv(candidates):

    with (REPORTS / "duplicate_candidates.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.writer(fp)

        writer.writerow(
            [
                "candidate",
                "count",
                "incoming",
                "outgoing",
                "layers",
                "components",
            ]
        )

        for item in candidates:

            writer.writerow(
                [
                    item["key"],
                    item["count"],
                    item["incoming"],
                    item["outgoing"],
                    ";".join(item["layers"]),
                    ";".join(item["components"]),
                ]
            )


# ============================================================================


def write_markdown(candidates):

    lines = [

        "# DELBot Duplicate Candidates",

        "",

        "## Summary",

        "",

        f"Groups : {len(candidates)}",

        "",

        "| Candidate | Count | In | Out | Layers |",

        "|------------|------:|---:|----:|--------|",

    ]

    for item in candidates:

        lines.append(

            f"| {item['key']} | "
            f"{item['count']} | "
            f"{item['incoming']} | "
            f"{item['outgoing']} | "
            f"{', '.join(item['layers'])} |"

        )

    (REPORTS / "duplicate_candidates.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ============================================================================


def main():

    ownership = load_json(
        "architecture_ownership.json",
    )

    groups = build_groups(
        ownership,
    )

    candidates = []

    for group in groups.values():

        item = classify(group)

        if item:

            candidates.append(item)

    candidates.sort(

        key=lambda x: (

            -x["count"],

            -x["incoming"],

            x["key"],

        )

    )

    write_json(candidates)

    write_csv(candidates)

    write_markdown(candidates)

    print()

    print("Duplicate candidates generated")

    print(f"Groups : {len(candidates)}")

    print()


if __name__ == "__main__":
    main()