from app.services.document.session_store import (
    ACTIVE_DOCUMENTS
)

def save_document(

    filename: str,

    content: str,

    chunks=None
):

    ACTIVE_DOCUMENTS["current"] = {

        "filename": filename,

        "content": content,

        "chunks": chunks or []

    }


def get_document():

    return ACTIVE_DOCUMENTS.get(
        "current"
    )