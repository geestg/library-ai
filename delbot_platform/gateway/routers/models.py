from fastapi import APIRouter

from delbot_platform.ai.registry.registry import ModelRegistry


router = APIRouter(
    prefix="/v1",
    tags=["Models"],
)


registry = ModelRegistry()


@router.get("/models")
def models():

    result = []

    for category in registry.categories():

        for name in registry.models(category):

            result.append(
                {
                    "id": name,
                    "object": "model",
                    "category": category,
                }
            )

    return {
        "object": "list",
        "data": result,
    }
