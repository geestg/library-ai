from __future__ import annotations

import csv
import json
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[2] / "reports"


# ==============================================================================
# LOAD
# ==============================================================================


def load_json(filename: str):

    with (REPORTS / filename).open(
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


# ==============================================================================
# BUILD LOOKUP
# ==============================================================================


def build_duplicate_lookup(rows):

    lookup = {}

    for item in rows:

        for module in item["modules"]:

            lookup[module] = {

                "group": item["key"],

                "count": item["count"],

            }

    return lookup


def build_merge_lookup(rows):

    lookup = {}

    for item in rows:

        for module in item["modules"]:

            lookup[module] = item

    return lookup


# ==============================================================================
# STATUS
# ==============================================================================


def status_of(recommendation):

    mapping = {

        "KEEP": "CANONICAL",

        "MERGE": "MERGE",

        "REVIEW": "REVIEW",

        "LEGACY": "LEGACY",

    }

    return mapping.get(

        recommendation,

        "UNKNOWN",

    )


# ==============================================================================
# BUILD
# ==============================================================================


def build():

    ownership = load_json(
        "architecture_ownership.json",
    )

    duplicates = load_json(
        "duplicate_candidates.json",
    )

    merge = load_json(
        "merge_recommendation.json",
    )

    duplicate_lookup = build_duplicate_lookup(
        duplicates,
    )

    merge_lookup = build_merge_lookup(
        merge,
    )

    rows = []

    for item in ownership:

        module = item["module"]

        duplicate = duplicate_lookup.get(
            module,
            {},
        )

        merge_item = merge_lookup.get(
            module,
            {},
        )

        recommendation = merge_item.get(

            "recommendation",

            "KEEP",

        )

        rows.append(

            {

                "module": module,

                "path": item["path"],

                "layer": item["layer"],

                "component": item["component"],

                "incoming": item["incoming"],

                "outgoing": item["outgoing"],

                "dependency_score": merge_item.get(
                    "dependency_score",
                    0,
                ),

                "ownership_score": merge_item.get(
                    "ownership_score",
                    1,
                ),

                "duplicate_group": duplicate.get(
                    "group",
                    "",
                ),

                "duplicate_count": duplicate.get(
                    "count",
                    1,
                ),

                "recommendation": recommendation,

                "status": status_of(
                    recommendation,
                ),

            }

        )

    rows.sort(

        key=lambda x: (

            x["status"],

            x["layer"],

            x["module"],

        )

    )

    return rows


# ==============================================================================
# JSON
# ==============================================================================


def write_json(rows):

    with (REPORTS / "architecture_index.json").open(

        "w",

        encoding="utf-8",

    ) as fp:

        json.dump(

            rows,

            fp,

            indent=4,

        )


# ==============================================================================
# CSV
# ==============================================================================


def write_csv(rows):

    with (REPORTS / "architecture_index.csv").open(

        "w",

        newline="",

        encoding="utf-8",

    ) as fp:

        writer = csv.DictWriter(

            fp,

            fieldnames=list(rows[0].keys()),

        )

        writer.writeheader()

        writer.writerows(rows)


# ==============================================================================
# MARKDOWN
# ==============================================================================


def write_markdown(rows):

    summary = {}

    for row in rows:

        summary.setdefault(

            row["status"],

            0,

        )

        summary[row["status"]] += 1

    lines = [

        "# DELBot Architecture Index",

        "",

        "## Summary",

        "",

        f"Modules : {len(rows)}",

        "",

        "| Status | Modules |",

        "|--------|---------|",

    ]

    for status in sorted(summary):

        lines.append(

            f"| {status} | {summary[status]} |"

        )

    lines.extend(

        [

            "",

            "## Layer Summary",

            "",

            "| Layer | Modules |",

            "|------|---------|",

        ]

    )

    layers = {}

    for row in rows:

        layers.setdefault(

            row["layer"],

            0,

        )

        layers[row["layer"]] += 1

    for layer in sorted(layers):

        lines.append(

            f"| {layer} | {layers[layer]} |"

        )

    (REPORTS / "architecture_index.md").write_text(

        "\n".join(lines),

        encoding="utf-8",

    )


# ==============================================================================
# MAIN
# ==============================================================================


def main():

    rows = build()

    write_json(rows)

    write_csv(rows)

    write_markdown(rows)

    print()

    print("Architecture index generated")

    print(f"Modules : {len(rows)}")

    print()


if __name__ == "__main__":

    main()
