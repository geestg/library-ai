from fastapi import APIRouter, UploadFile
from pathlib import Path
import shutil


from delbot_platform.document.pipeline import DocumentPipeline


router=APIRouter(
    prefix="/documents",
    tags=["documents"]
)


pipeline=DocumentPipeline()


@router.post("/upload")
async def upload(
    file:UploadFile
):

    target=Path(
        "repository/raw"
    ) / file.filename


    with target.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    result=pipeline.process(
        str(target)
    )


    return result
