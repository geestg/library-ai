from fastapi import APIRouter

from app.services.title_generator_service import (
    generate_thesis_titles
)

router = APIRouter(
    prefix="/thesis-title-generator",
    tags=["Research Intelligence"]
)


@router.post("")
def thesis_title_generator(
    payload: dict
):

    topic = payload.get(
        "topic",
        ""
    )

    return generate_thesis_titles(
        topic=topic
    )