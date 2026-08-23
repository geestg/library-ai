from __future__ import annotations

from pydantic import BaseModel


class DocumentIndexRequest(BaseModel):

    pdf_path: str