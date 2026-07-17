from __future__ import annotations


from pydantic import BaseModel



class RepositoryRegisterRequest(
    BaseModel
):
    """
    Request untuk mendaftarkan repository eksternal.
    """

    id: str

    name: str

    url: str

    type: str



class RepositoryIngestRequest(
    BaseModel
):
    """
    Request untuk menjalankan ingestion
    terhadap repository item.
    """

    item_id: str



class RepositoryStatusResponse(
    BaseModel
):
    """
    Generic repository response.
    """

    status: str

    message: str



class RepositoryIndexResponse(
    BaseModel
):
    """
    Response hasil indexing document.
    """

    status: str

    document_id: str

    chunks: int

    vectors: int

    message: str



__all__ = [

    "RepositoryRegisterRequest",

    "RepositoryIngestRequest",

    "RepositoryStatusResponse",

    "RepositoryIndexResponse",

]