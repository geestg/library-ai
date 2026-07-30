from __future__ import annotations

import csv
import json
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[2] / "reports"


def load_json(filename: str):
    with (REPORTS / filename).open(encoding="utf-8") as fp:
        return json.load(fp)


def classify(module: dict):

    incoming = module["incoming"]
    outgoing = module["outgoing"]
    status = module["status"]

    if status == "CANONICAL":
        return "KEEP", "Canonical module"

    if status == "REVIEW":
        return "MANUAL", "Architecture review required"

    if status == "MERGE":
        return "MERGE", "Merge before removal"

    if status != "LEGACY":
        return "KEEP", "No action"

    if incoming > 0:
        return "BLOCKED", "Referenced by other modules"

    if outgoing > 0:
        return "VERIFY", "Depends on other modules"

    return "SAFE_REMOVE", "Isolated legacy module"


def build():

    index = load_json(
        "architecture_index.json",
    )

    rows = []

    for module in index:

        action, reason = classify(module)

        rows.append(
            {
                "module": module["module"],
                "path": module["path"],
                "layer": module["layer"],
                "status": module["status"],
                "incoming": module["incoming"],
                "outgoing": module["outgoing"],
                "action": action,
                "reason": reason,
            }
        )

    rows.sort(
        key=lambda r: (
            r["action"],
            r["layer"],
            r["module"],
        )
    )

    return rows


def write_json(rows):

    with (REPORTS / "safe_removal_plan.json").open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            rows,
            fp,
            indent=4,
        )


def write_csv(rows):

    with (REPORTS / "safe_removal_plan.csv").open(
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

        "# DELBot Safe Removal Plan",

        "",

        "## Summary",

        "",

        f"Modules : {len(rows)}",

        "",

        "| Action | Count |",

        "|--------|------:|",

    ]

    for key in sorted(summary):

        lines.append(
            f"| {key} | {summary[key]} |"
        )

    lines.extend(
        [
            "",
            "## Candidates",
            "",
            "| Module | Action | Incoming | Outgoing |",
            "|--------|--------|---------:|---------:|",
        ]
    )

    for row in rows:

        if row["action"] == "KEEP":
            continue

        lines.append(
            f"| {row['module']} | "
            f"{row['action']} | "
            f"{row['incoming']} | "
            f"{row['outgoing']} |"
        )

    (REPORTS / "safe_removal_plan.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():

    rows = build()

    write_json(rows)
    write_csv(rows)
    write_markdown(rows)

    print()
    print("Safe removal plan generated")
    print(f"Modules : {len(rows)}")
    print()


if __name__ == "__main__":
    main()
