import sys

from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]


sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.document.pipeline.ingest_pdf import (
    PDFIngestion
)



pdf=list(
    Path(
        "delbot_platform/repository_data/thesis_files"
    ).glob(
        "*.pdf"
    )
)[0]



service=PDFIngestion()


result=service.ingest(
    str(pdf)
)


print(result)
