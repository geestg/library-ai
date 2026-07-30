from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[2] / "reports"


def load_json(filename: str):

    with (REPORTS / filename).open(
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


def package_name(module: str) -> str:

    parts = module.split(".")

    if len(parts) >= 3:
        return parts[2]

    return "other"


def build():

    index = load_json(
        "architecture_index.json",
    )

    packages = defaultdict(
        lambda: {
            "modules": 0,
            "canonical": 0,
            "merge": 0,
            "review": 0,
            "legacy": 0,
            "layers": set(),
            "components": set(),
        }
    )

    for row in index:

        pkg = package_name(
            row["module"],
        )

        info = packages[pkg]

        info["modules"] += 1

        info["layers"].add(
            row["layer"],
        )

        info["components"].add(
            row["component"],
        )

        status = row["status"]

        if status == "CANONICAL":
            info["canonical"] += 1

        elif status == "MERGE":
            info["merge"] += 1

        elif status == "REVIEW":
            info["review"] += 1

        elif status == "LEGACY":
            info["legacy"] += 1

    rows = []

    for package, info in sorted(packages.items()):

        rows.append({

            "package": package,

            "modules": info["modules"],

            "canonical": info["canonical"],

            "merge": info["merge"],

            "review": info["review"],

            "legacy": info["legacy"],

            "layers": sorted(info["layers"]),

            "components": sorted(info["components"]),

        })

    return rows


def write_json(rows):

    with (REPORTS / "package_detector.json").open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            rows,
            fp,
            indent=4,
        )


def write_csv(rows):

    with (REPORTS / "package_detector.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fp:

        writer = csv.writer(fp)

        writer.writerow([
            "package",
            "modules",
            "canonical",
            "merge",
            "review",
            "legacy",
        ])

        for row in rows:

            writer.writerow([
                row["package"],
                row["modules"],
                row["canonical"],
                row["merge"],
                row["review"],
                row["legacy"],
            ])


def write_markdown(rows):

    lines = [

        "# DELBot Package Detector",

        "",

        "## Packages",

        "",

        "| Package | Modules | Canonical | Merge | Review | Legacy |",

        "|---------|--------:|----------:|------:|-------:|-------:|",

    ]

    for row in rows:

        lines.append(

            f"| {row['package']} | "
            f"{row['modules']} | "
            f"{row['canonical']} | "
            f"{row['merge']} | "
            f"{row['review']} | "
            f"{row['legacy']} |"

        )

    (REPORTS / "package_detector.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():

    rows = build()

    write_json(rows)

    write_csv(rows)

    write_markdown(rows)

    print()
    print("Package detector generated")
    print(f"Packages : {len(rows)}")
    print()


if __name__ == "__main__":
    main()
