import sys

from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]


sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.document.pipeline.pdf_loader import (
    PDFLoader
)



pdf=list(
    Path(
        "delbot_platform/repository_data/thesis_files"
    ).glob(
        "*.pdf"
    )
)[0]


loader=PDFLoader()


pages=loader.load(
    str(pdf)
)


print(
    "PDF:",
    pdf
)


print(
    "PAGES:",
    len(pages)
)


for p in pages[:3]:

    print("================")

    print(
        p["page"]
    )

    print(
        p["text"][:300]
    )
