from __future__ import annotations


from pathlib import Path
import time


from delbot_platform.document.pipeline.ingest_pdf import PDFIngestion



PDF_DIR = Path(
    "delbot_platform/repository_data/thesis_files"
)



def main():


    pdfs = list(
        PDF_DIR.glob(
            "*.pdf"
        )
    )


    print(
        "TOTAL PDF:",
        len(pdfs)
    )


    pipeline = PDFIngestion()


    success = 0
    failed = 0


    start=time.time()



    for index,pdf in enumerate(pdfs,1):


        print(
            "\n=============================="
        )

        print(
            f"[{index}/{len(pdfs)}]",
            pdf.name
        )


        try:


            result=pipeline.ingest(
                str(pdf)
            )


            print(
                "RESULT:",
                result
            )


            success += 1



        except Exception as e:


            failed += 1


            print(
                "FAILED:",
                pdf.name
            )


            print(
                e
            )



    elapsed=time.time()-start



    print(
        "\n========== FINISH =========="
    )


    print(
        "SUCCESS:",
        success
    )


    print(
        "FAILED:",
        failed
    )


    print(
        "TIME:",
        elapsed
    )



if __name__=="__main__":

    main()
