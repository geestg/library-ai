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
# SCORE
# ==============================================================================


def dependency_score(item):

    return (
        item["incoming"] * 2
        +
        item["outgoing"]
    )


def ownership_score(item):

    return len(
        item["layers"]
    )


# ==============================================================================
# RECOMMENDATION
# ==============================================================================


def recommend(item):

    dep = dependency_score(item)

    own = ownership_score(item)

    count = item["count"]

    if count <= 1:
        return (
            "KEEP",
            "Single implementation",
        )

    if own == 1:
        return (
            "KEEP",
            "Same architectural layer",
        )

    if dep >= 20:
        return (
            "REVIEW",
            "High dependency impact",
        )

    if dep >= 8:
        return (
            "MERGE",
            "Moderate dependency",
        )

    return (
        "LEGACY",
        "Low dependency duplicate",
    )


# ==============================================================================
# BUILD
# ==============================================================================


def build():

    duplicates = load_json(
        "duplicate_candidates.json",
    )

    rows = []

    for item in duplicates:

        recommendation, reason = recommend(
            item,
        )

        rows.append(

            {

                "canonical_name": item["key"],

                "count": item["count"],

                "layers": item["layers"],

                "components": item["components"],

                "dependency_score": dependency_score(
                    item,
                ),

                "ownership_score": ownership_score(
                    item,
                ),

                "recommendation": recommendation,

                "reason": reason,

                "modules": item["modules"],

            }

        )

    return sorted(

        rows,

        key=lambda x: (

            x["recommendation"],

            -x["dependency_score"],

            x["canonical_name"],

        ),

    )


# ==============================================================================
# JSON
# ==============================================================================


def write_json(rows):

    with (REPORTS / "merge_recommendation.json").open(

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

    with (REPORTS / "merge_recommendation.csv").open(

        "w",

        newline="",

        encoding="utf-8",

    ) as fp:

        writer = csv.writer(fp)

        writer.writerow(

            [

                "canonical_name",

                "recommendation",

                "dependency_score",

                "ownership_score",

                "count",

                "layers",

            ]

        )

        for row in rows:

            writer.writerow(

                [

                    row["canonical_name"],

                    row["recommendation"],

                    row["dependency_score"],

                    row["ownership_score"],

                    row["count"],

                    ";".join(row["layers"]),

                ]

            )


# ==============================================================================
# MARKDOWN
# ==============================================================================


def write_markdown(rows):

    lines = [

        "# DELBot Merge Recommendation",

        "",

        "## Summary",

        "",

        f"Candidates : {len(rows)}",

        "",

        "| Name | Recommendation | Score | Ownership | Count |",

        "|------|----------------|------:|----------:|------:|",

    ]

    for row in rows:

        lines.append(

            f"| {row['canonical_name']} | "

            f"{row['recommendation']} | "

            f"{row['dependency_score']} | "

            f"{row['ownership_score']} | "

            f"{row['count']} |"

        )

    (REPORTS / "merge_recommendation.md").write_text(

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

    print("Merge recommendation generated")

    print(f"Candidates : {len(rows)}")

    print()


if __name__ == "__main__":

    main()
