import sys

from pathlib import Path

from concurrent.futures import ProcessPoolExecutor, as_completed


ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(ROOT)
)


from delbot_platform.document.pipeline.ingest_pdf import PDFIngestion



PDF_DIR = Path(
    "delbot_platform/repository_data/thesis_files"
)


METADATA = (
    "delbot_platform/repository_data/metadata/skripsi_dataset.json"
)



def process_pdf(pdf):

    try:

        engine = PDFIngestion(
            METADATA
        )


        return engine.ingest(
            str(pdf)
        )


    except Exception as e:

        return {

            "file":str(pdf),

            "error":str(e)

        }



def main():


    files=list(
        PDF_DIR.glob(
            "*.pdf"
        )
    )


    print(
        "TOTAL:",
        len(files)
    )


    with ProcessPoolExecutor(
        max_workers=2
    ) as executor:


        futures=[

            executor.submit(
                process_pdf,
                f
            )

            for f in files

        ]


        for future in as_completed(futures):

            print(
                future.result()
            )




if __name__=="__main__":

    main()
