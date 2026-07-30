from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from delbot_platform.documents.classification.heading import HeadingClassifier
from delbot_platform.documents.extraction.service import DocumentExtractionService
from delbot_platform.documents.models.block import Block

ROOT = Path("delbot_platform/repository_data/pdf")

TITLE_FP = (
    "TUGAS AKHIR",
    "SKRIPSI",
    "TESIS",
    "DOKUMEN TUGAS AKHIR",
    "OLEH",
    "PROGRAM STUDI",
)

AUTHOR_FP = (
    "LAGUBOTI",
    "PROGRAM STUDI",
    "DOKUMEN TUGAS AKHIR",
    "LOGIC CONTROLLER",
    "FAKULTAS",
    "INSTITUT",
)

DATE_FP = (
    "PROGRAM STUDI",
    "FAKULTAS",
)


def iter_pdfs():
    yield from sorted(ROOT.rglob("*.pdf"))


def suspicious(text: str, patterns) -> bool:
    upper = text.upper()
    return any(x in upper for x in patterns)


def audit_pdf(path: Path, classifier: HeadingClassifier):
    extractor = DocumentExtractionService()

    blocks: list[Block] = extractor.extract(str(path))

    classifier.classify_all(blocks)

    counter = Counter()

    samples = defaultdict(list)

    fp = defaultdict(list)

    for block in blocks:

        name = block.type.name

        counter[name] += 1

        if len(samples[name]) < 5:
            samples[name].append(block.text.strip())

        text = block.text.strip()

        if name == "TITLE" and suspicious(text, TITLE_FP):
            if len(fp["TITLE"]) < 20:
                fp["TITLE"].append(text)

        elif name == "AUTHOR" and suspicious(text, AUTHOR_FP):
            if len(fp["AUTHOR"]) < 20:
                fp["AUTHOR"].append(text)

        elif name == "DATE" and suspicious(text, DATE_FP):
            if len(fp["DATE"]) < 20:
                fp["DATE"].append(text)

    return counter, samples, fp


def merge_counter(dst, src):
    dst.update(src)


def merge_list(dst, src):
    for key, values in src.items():
        for value in values:
            if value not in dst[key]:
                dst[key].append(value)


def print_section(title, values):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    if not values:
        print("(none)")
        return

    for item in values:
        print("-", item.replace("\n", " ")[:120])


def main():

    classifier = HeadingClassifier()

    totals = Counter()

    samples = defaultdict(list)

    fp = defaultdict(list)

    pdfs = 0

    print("=" * 60)
    print("DELBot Regression Heading Audit")
    print("=" * 60)

    for pdf in iter_pdfs():

        pdfs += 1

        try:
            c, s, f = audit_pdf(pdf, classifier)

            merge_counter(totals, c)
            merge_list(samples, s)
            merge_list(fp, f)

        except Exception as exc:
            print(f"[ERROR] {pdf.name}: {exc}")

    print()
    print(f"PDF Repository : {pdfs}")
    print()

    order = (
        "TITLE",
        "AUTHOR",
        "DATE",
        "INSTITUTION",
        "HEADING",
        "PARAGRAPH",
        "UNKNOWN",
    )

    for key in order:
        print(f"{key:12}: {totals.get(key,0)}")

    for key in order:
        print_section(f"Sample {key}", samples[key])

    print_section("Potential TITLE False Positive", fp["TITLE"])
    print_section("Potential AUTHOR False Positive", fp["AUTHOR"])
    print_section("Potential DATE False Positive", fp["DATE"])


if __name__ == "__main__":
    main()