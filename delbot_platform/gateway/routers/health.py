import torch

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health():

    gpu = None

    if torch.cuda.is_available():
        gpu = torch.cuda.get_device_name(0)

    return {
        "status": "healthy",
        "gpu": gpu,
        "cuda": torch.version.cuda,
        "torch": torch.__version__,
    }
