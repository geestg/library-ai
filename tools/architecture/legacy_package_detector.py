from __future__ import annotations

import csv
import json
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[2] / "reports"


def load_json(filename: str):

    with (REPORTS / filename).open(
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


def classify(package):

    modules = package["modules"]

    canonical = package["canonical"]

    merge = package["merge"]

    review = package["review"]

    legacy = package["legacy"]

    if legacy == modules:
        return (
            "REMOVE",
            "Entire package marked legacy",
        )

    if canonical == modules:
        return (
            "KEEP",
            "Entire package canonical",
        )

    if review > 0:
        return (
            "REVIEW",
            "Manual verification required",
        )

    if merge > 0:
        return (
            "MERGE",
            "Merge candidates detected",
        )

    if legacy > 0:
        return (
            "PARTIAL",
            "Contains legacy modules",
        )

    return (
        "KEEP",
        "Healthy package",
    )


def build():

    packages = load_json(
        "package_detector.json",
    )

    rows = []

    for package in packages:

        action, reason = classify(package)

        rows.append({

            "package": package["package"],

            "modules": package["modules"],

            "canonical": package["canonical"],

            "merge": package["merge"],

            "review": package["review"],

            "legacy": package["legacy"],

            "action": action,

            "reason": reason,

        })

    rows.sort(

        key=lambda x: (

            x["action"],

            -x["legacy"],

            x["package"],

        )

    )

    return rows


def write_json(rows):

    with (REPORTS / "legacy_package_detector.json").open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            rows,
            fp,
            indent=4,
        )


def write_csv(rows):

    with (REPORTS / "legacy_package_detector.csv").open(
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


def write_markdown(rows):

    summary = {}

    for row in rows:

        summary.setdefault(
            row["action"],
            0,
        )

        summary[row["action"]] += 1

    lines = [

        "# DELBot Legacy Package Detector",

        "",

        "## Summary",

        "",

        f"Packages : {len(rows)}",

        "",

        "| Action | Packages |",

        "|--------|----------|",

    ]

    for action in sorted(summary):

        lines.append(

            f"| {action} | {summary[action]} |"

        )

    lines.extend(

        [

            "",

            "## Packages",

            "",

            "| Package | Action | Legacy | Merge | Review |",

            "|---------|--------|-------:|------:|-------:|",

        ]

    )

    for row in rows:

        lines.append(

            f"| {row['package']} | "
            f"{row['action']} | "
            f"{row['legacy']} | "
            f"{row['merge']} | "
            f"{row['review']} |"

        )

    (REPORTS / "legacy_package_detector.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():

    rows = build()

    write_json(rows)

    write_csv(rows)

    write_markdown(rows)

    print()

    print("Legacy package detector generated")

    print(f"Packages : {len(rows)}")

    print()


if __name__ == "__main__":
    main()
