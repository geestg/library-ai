from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile

from delbot_platform.documents.services import (
    DocumentIndexService,
)


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


service = DocumentIndexService()


@router.post("/upload")
async def upload(
    file: UploadFile,
):

    target = (
        Path("repository/raw")
        / file.filename
    )

    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with target.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    artifact, summary = (
        await service.index(
            str(target),
        )
    )

    return {
        "success": summary.success,
        "summary": summary,
    }
