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



pdf=Path(
"delbot_platform/repository_data/thesis_files/0ff47c59f90b4881a36395bcb4dd508b.pdf"
)



loader=PDFLoader()


pages=loader.load(
    str(pdf)
)



print(
    "TOTAL PAGE:",
    len(pages)
)



for page in pages[:2]:

    print("================")

    print(
        page["page"]
    )

    print(
        page["text"][:500]
    )
