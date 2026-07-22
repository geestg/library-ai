import json

from pathlib import Path



PDF_DIR=Path(
"delbot_platform/repository_data/thesis_files"
)


OUTPUT=Path(
"delbot_platform/repository_data/metadata/pdf_index.json"
)



items=[]


for pdf in PDF_DIR.glob(
"*.pdf"
):


    items.append(

        {
            "file":str(pdf),
            "id":pdf.stem
        }

    )


OUTPUT.write_text(

    json.dumps(
        items,
        indent=2
    ),

    encoding="utf-8"

)


print(
"INDEX:",
len(items)
)
